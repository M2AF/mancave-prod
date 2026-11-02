Add-Type -AssemblyName System.Drawing
$views = @('home','chainlens','magic-money','afterglow','arcade')
foreach ($width in @(1440,768,390,320)) {
    $canvas = [System.Drawing.Bitmap]::new(1500,2235)
    $graphics = [System.Drawing.Graphics]::FromImage($canvas)
    $graphics.Clear([System.Drawing.Color]::LightGray)
    $font = [System.Drawing.Font]::new('Arial',12)
    for ($i=0; $i -lt $views.Count; $i++) {
        $name = "$width-$($views[$i]).png"
        $source = [System.Drawing.Image]::FromFile((Join-Path $PSScriptRoot $name))
        $scale = [Math]::Min(300.0/$source.Width,2200.0/$source.Height)
        $dest = [System.Drawing.Rectangle]::new(($i*300),30,[int]($source.Width*$scale),[int]($source.Height*$scale))
        $graphics.DrawString($name,$font,[System.Drawing.Brushes]::Black,($i*300),0)
        $graphics.DrawImage($source,$dest)
        $source.Dispose()
    }
    $canvas.Save((Join-Path $PSScriptRoot "contact-$width.png"),[System.Drawing.Imaging.ImageFormat]::Png)
    $font.Dispose()
    $graphics.Dispose()
    $canvas.Dispose()
}
