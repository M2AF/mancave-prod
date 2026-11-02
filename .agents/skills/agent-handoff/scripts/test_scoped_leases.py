"""Resource-lease regressions on temporary boards; no live project mutation."""
import contextlib
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import handoff as h
import scoped_leases as s


class ScopedLeaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ("main", "one", "two"):
            (self.root / name).mkdir()
        self.git = patch.object(h, "git_state", return_value=("abc123", "(test) clean"))
        self.git.start()
        self.call("init", "--repo", "main")
        self.call("claim", "claude", "ft_donkey shoulder_start", "--resource", "fighter/ft_donkey")

    def tearDown(self):
        self.git.stop()
        self.temp.cleanup()

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return h.main(["--dir", str(self.root), *args])

    def claim(self, owner="codex", id="codex-one", repo="one", resource="fighter/ft_purin"):
        return self.call("lease-claim", owner, id, "small fighter unit", "--repo", repo, "--resource", resource)

    def test_disjoint_worktree_and_fighter_coexist_with_main(self):
        before = (self.root / h.BOARD).read_bytes()
        self.assertEqual(self.claim(), 0)
        self.assertEqual((self.root / h.BOARD).read_bytes(), before)
        self.assertEqual(len(s.load(self.root)["leases"]), 1)

    def test_same_fighter_is_rejected_even_in_different_worktree(self):
        self.assertEqual(self.claim(resource="fighter/ft_donkey"), 2)

    def test_same_checkout_is_rejected_even_for_other_fighter(self):
        self.assertEqual(self.claim(repo="main"), 2)

    def test_parallel_same_resource_is_rejected(self):
        self.assertEqual(self.claim(), 0)
        self.assertEqual(self.claim(owner="claude", id="other", repo="two"), 2)

    def test_resource_parent_conflicts_with_child(self):
        self.assertEqual(self.claim(resource="shared/include/ft"), 0)
        self.assertEqual(self.claim(owner="claude", id="other", repo="two", resource="shared/include/ft/grab.h"), 2)

    def test_legacy_main_claim_cannot_enter_parallel_fighter(self):
        self.assertEqual(self.claim(), 0)
        before = (self.root / h.BOARD).read_bytes()
        self.assertEqual(self.call("claim", "claude", "ft_purin final", "--resource", "fighter/ft_purin"), 2)
        self.assertEqual((self.root / h.BOARD).read_bytes(), before)

    def test_unknown_legacy_task_blocks_parallel_conservatively(self):
        self.assertEqual(self.call("claim", "claude", "unknown broad task"), 0)
        self.assertEqual(self.claim(), 2)

    def test_force_does_not_bypass_scoped_conflicts(self):
        self.assertEqual(self.claim(), 0)
        self.assertEqual(self.call("claim", "claude", "integrate", "--force"), 2)

    def test_log_and_release_preserve_main_board_and_next(self):
        self.assertEqual(self.claim(), 0)
        before = (self.root / h.BOARD).read_bytes()
        self.assertEqual(self.call("lease-log", "codex", "codex-one", "-m", "matched", "--verified", "127/127", "--next", "probe"), 0)
        self.assertIn("127/127", s.load(self.root)["leases"]["codex-one"]["verified"])
        self.assertEqual(self.call("lease-release", "codex", "codex-one", "--next", "integrator pickup"), 0)
        self.assertEqual((self.root / h.BOARD).read_bytes(), before)
        self.assertFalse(s.load(self.root)["leases"])

    def test_wrong_owner_cannot_log_release_or_replace(self):
        self.assertEqual(self.claim(), 0)
        self.assertEqual(self.call("lease-log", "claude", "codex-one", "-m", "overwrite"), 2)
        self.assertEqual(self.call("lease-release", "claude", "codex-one"), 2)
        self.assertEqual(self.claim(owner="claude"), 2)

    def test_expired_lease_must_reclaim_before_logging(self):
        self.assertEqual(self.claim(), 0)
        state = s.load(self.root)
        state["leases"]["codex-one"]["lease_until"] = (dt.datetime.now().astimezone() - dt.timedelta(hours=1)).isoformat()
        h.write_atomic(self.root / s.FILE, json.dumps(state))
        self.assertEqual(self.call("lease-log", "codex", "codex-one", "-m", "late"), 2)
        self.assertEqual(self.claim(owner="claude"), 0)

    def test_integration_gate_requires_parallel_release(self):
        self.assertEqual(self.claim(), 0)
        self.assertEqual(self.call("leases", "--require-clear"), 2)
        self.assertEqual(self.call("lease-release", "codex", "codex-one"), 0)
        self.assertEqual(self.call("leases", "--require-clear"), 0)

    def test_corrupt_registry_fails_closed(self):
        (self.root / s.FILE).write_text("{broken")
        self.assertEqual(self.claim(), 2)
        self.assertEqual(self.call("claim", "claude", "ft_donkey next"), 2)

    def test_exclusive_integration_gate_blocks_new_claims(self):
        self.assertEqual(self.call("leases", "--require-integration"), 2)
        self.assertEqual(self.call("claim", "claude", "integration of ready branches"), 0)
        self.assertEqual(self.call("leases", "--require-integration"), 0)
        self.assertEqual(self.claim(), 2)

    def test_rejects_invalid_hours_and_paths(self):
        self.assertEqual(self.call("lease-claim", "codex", "x", "unit", "--repo", "missing", "--resource", "fighter/ft_purin"), 2)
        self.assertEqual(self.call("lease-claim", "codex", "x", "unit", "--repo", "one", "--resource", "fighter/ft_purin", "--hours", "nan"), 2)
        self.assertEqual(self.claim(resource="fighter/../ft_purin"), 2)

    def test_two_concurrent_claims_only_one_wins(self):
        barrier = threading.Barrier(2)
        results = []
        def compete(index):
            from types import SimpleNamespace
            barrier.wait()
            args = SimpleNamespace(cmd="lease-claim", agent=f"worker{index}", id=f"worker{index}",
                task="same fighter", repo="one" if index == 1 else "two", resource=["fighter/ft_purin"], hours=1)
            results.append(s.run(self.root, args, h))
        threads = [threading.Thread(target=compete, args=(i,)) for i in (1, 2)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        self.assertEqual(sorted(results), [0, 2])
        self.assertEqual(len(s.load(self.root)["leases"]), 1)


if __name__ == "__main__":
    unittest.main()
