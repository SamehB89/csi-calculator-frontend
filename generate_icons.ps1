
Add-Type -AssemblyName System.Drawing

$sourcePath = "d:\SUPERMANn\CSI_Project\frontend\assets\icon-1024.jpg"
$destDir = "d:\SUPERMANn\CSI_Project\frontend\assets"

$img = [System.Drawing.Image]::FromFile($sourcePath)

function Resize-Image {
    param([int]$w, [int]$h, [string]$name)
    $rect = New-Object System.Drawing.Rectangle 0, 0, $w, $h
    $dest = New-Object System.Drawing.Bitmap $w, $h
    $dest.SetResolution($img.HorizontalResolution, $img.VerticalResolution)
    $g = [System.Drawing.Graphics]::FromImage($dest)
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.DrawImage($img, $rect)
    $dest.Save("$destDir\$name", [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $dest.Dispose()
    Write-Host "Created $name"
}

Resize-Image 512 512 "icon-512.png"
Resize-Image 192 192 "icon-192.png"

$img.Dispose()
