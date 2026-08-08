# download_fonts.ps1
# Save this file as UTF-8 with BOM if you see encoding errors.

$null = New-Item -ItemType Directory -Force -Path "fonts"

$wbPrefix = "https://web.archive.org/web/20260408000823/"

$fontUrls = @(
    "https://sourcebucket.s3.bitiful.net/fonts/优设好身体.woff2",
    "https://sourcebucket.s3.bitiful.net/fonts/MiSans.woff2",
    "https://sourcebucket.s3.bitiful.net/fonts/HYTangMeiRen55W.woff2",
    "https://sourcebucket.s3.bitiful.net/fonts/霞鹜文楷.woff2",
    "https://sourcebucket.s3.bitiful.net/fonts/甜甜圈海报字体.woff2",
    "https://files.xzy404.me/fonts/JetBrainsMono-Light.woff2",
    "https://sourcebucket.s3.bitiful.net/fonts/ZhuZiAWan2.woff2"
)

Write-Host "Starting download..." -ForegroundColor Cyan

foreach ($url in $fontUrls) {
    $fileName = [System.IO.Path]::GetFileName($url)
    $localPath = Join-Path "fonts" $fileName

    if ($url -like "*sourcebucket.s3.bitiful.net*") {
        $uri = [System.Uri]$url
        $escapedFileName = [System.Uri]::EscapeDataString($fileName)
        $encodedUrl = $url -replace [System.Text.RegularExpressions.Regex]::Escape($fileName), $escapedFileName
        $downloadUrl = $wbPrefix + $encodedUrl
    } else {
        $downloadUrl = $url
    }

    Write-Host "Downloading: $fileName" -ForegroundColor Yellow
    Write-Host "  From: $downloadUrl"

    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $localPath -ErrorAction Stop
        Write-Host "  [OK]" -ForegroundColor Green
    } catch {
        Write-Host "  [FAIL] $_" -ForegroundColor Red
        if (Test-Path $localPath) { Remove-Item $localPath }
    }
    Write-Host ""
}

Write-Host "All downloads completed. Check the 'fonts' folder." -ForegroundColor Cyan