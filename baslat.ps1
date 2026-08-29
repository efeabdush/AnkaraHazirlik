$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$script:api = $null
$script:web = $null
$script:stopping = $false
$logDir = Join-Path $PSScriptRoot ".runlogs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$apiLog = Join-Path $logDir "api.log"
$webLog = Join-Path $logDir "web.log"

function Stop-Children {
  if ($script:stopping) { return }
  $script:stopping = $true

  foreach ($proc in @($script:web, $script:api)) {
    if ($null -eq $proc) { continue }
    try {
      if (-not $proc.HasExited) {
        & taskkill.exe /PID $proc.Id /T /F 2>$null | Out-Null
      }
    } catch {}
  }

  # Portlari da temizle (yetim process kalmasin)
  foreach ($port in 8000, 3000) {
    try {
      $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
      foreach ($c in $conns) {
        if ($c.OwningProcess) {
          & taskkill.exe /PID $c.OwningProcess /T /F 2>$null | Out-Null
        }
      }
    } catch {}
  }
}

function Free-Port {
  param([int]$Port)
  try {
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  } catch {
    return
  }
  foreach ($c in $conns) {
    if (-not $c.OwningProcess) { continue }
    Write-Host ("[baslat] Port {0} dolu (PID {1}), kapatiliyor..." -f $Port, $c.OwningProcess)
    & taskkill.exe /PID $c.OwningProcess /T /F 2>$null | Out-Null
  }
}

function Wait-Http {
  param([string]$Url, [int]$Seconds = 40)
  $deadline = (Get-Date).AddSeconds($Seconds)
  while ((Get-Date) -lt $deadline) {
    try {
      $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
      if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { return $true }
    } catch {}
    Start-Sleep -Milliseconds 400
  }
  return $false
}

function Start-LoggedProcess {
  param(
    [string]$FileName,
    [string]$Arguments,
    [string]$WorkingDirectory,
    [string]$LogFile
  )

  if (Test-Path $LogFile) { Remove-Item $LogFile -Force -ErrorAction SilentlyContinue }

  $info = New-Object System.Diagnostics.ProcessStartInfo
  $info.FileName = $FileName
  $info.Arguments = $Arguments
  $info.WorkingDirectory = $WorkingDirectory
  $info.UseShellExecute = $false
  $info.RedirectStandardOutput = $true
  $info.RedirectStandardError = $true
  $info.CreateNoWindow = $true

  $proc = New-Object System.Diagnostics.Process
  $proc.StartInfo = $info
  $proc.EnableRaisingEvents = $true

  $writer = {
    if ($EventArgs.Data) {
      $line = $EventArgs.Data
      Add-Content -Path $Event.MessageData -Value $line -Encoding UTF8
      Write-Host $line
    }
  }

  Register-ObjectEvent -InputObject $proc -EventName OutputDataReceived -MessageData $LogFile -Action $writer | Out-Null
  Register-ObjectEvent -InputObject $proc -EventName ErrorDataReceived -MessageData $LogFile -Action $writer | Out-Null

  if (-not $proc.Start()) {
    throw "Process baslatilamadi: $FileName"
  }
  $proc.BeginOutputReadLine()
  $proc.BeginErrorReadLine()
  return $proc
}

Write-Host ""
Write-Host "Hazirlik Prep"
Write-Host "Site:  http://localhost:3000"
Write-Host "Admin: http://localhost:3000/admin"
Write-Host ""
Write-Host "Bu pencere acik kalsin. Durdurmak icin Ctrl+C."
Write-Host ""

try {
  Write-Host "[baslat] Eski takili surecler temizleniyor..."
  Free-Port 3000
  Free-Port 3001
  Free-Port 8000
  Start-Sleep -Seconds 1

  $uvicorn = Join-Path $PSScriptRoot "backend\.venv\Scripts\uvicorn.exe"
  if (-not (Test-Path $uvicorn)) {
    throw "uvicorn bulunamadi: $uvicorn"
  }

  Write-Host "[baslat] API aciliyor..."
  $script:api = Start-LoggedProcess `
    -FileName $uvicorn `
    -Arguments "app.main:app --reload --port 8000 --host 127.0.0.1" `
    -WorkingDirectory (Join-Path $PSScriptRoot "backend") `
    -LogFile $apiLog

  Start-Sleep -Seconds 1
  if ($script:api.HasExited) {
    throw "API hemen kapandi. Log: $apiLog"
  }

  $npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
  if (-not $npm) {
    throw "npm.cmd bulunamadi. Node.js kurulu mu?"
  }

  # cmd.exe ile baslat: npm.cmd batch oldugu icin daha guvenilir
  Write-Host "[baslat] Site aciliyor..."
  $frontend = Join-Path $PSScriptRoot "frontend"
  $script:web = Start-LoggedProcess `
    -FileName "$env:ComSpec" `
    -Arguments "/d /c `"npm.cmd run dev`"" `
    -WorkingDirectory $frontend `
    -LogFile $webLog

  Start-Sleep -Seconds 2
  if ($script:web.HasExited) {
    throw "Site hemen kapandi. Log: $webLog"
  }

  Write-Host "[baslat] Site ayaga kalksin diye bekleniyor..."
  $apiOk = Wait-Http "http://127.0.0.1:8000/api/health" 20
  $webOk = Wait-Http "http://127.0.0.1:3000" 40
  if (-not $apiOk) { Write-Host "[uyari] API 8000 yanit vermiyor. Log: $apiLog" }
  if (-not $webOk) { throw "Site http://localhost:3000 yanit vermiyor. Log: $webLog" }

  Start-Process "http://localhost:3000" | Out-Null

  Write-Host ""
  Write-Host "Calisiyor. Bu pencereyi kapatma. Durdurmak icin Ctrl+C."
  Write-Host ""

  # Onemli: servis dusse bile pencere KAPANMAZ; Ctrl+C bekler.
  while (-not $script:stopping) {
    if ($script:api -and $script:api.HasExited) {
      Write-Host "[uyari] API kapandi (kod $($script:api.ExitCode)). Log: $apiLog"
      Write-Host "        Pencere acik kalacak. Ctrl+C ile cik."
      $script:api = $null
    }
    if ($script:web -and $script:web.HasExited) {
      Write-Host "[uyari] Site kapandi (kod $($script:web.ExitCode)). Log: $webLog"
      Write-Host "        Pencere acik kalacak. Ctrl+C ile cik."
      $script:web = $null
    }
    Start-Sleep -Seconds 1
  }
}
catch {
  Write-Host ""
  Write-Host ("Hata: " + $_.Exception.Message)
  Write-Host "Pencereyi kapatmak icin bir tusa bas..."
  try { $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") } catch { Start-Sleep -Seconds 8 }
}
finally {
  Write-Host ""
  Write-Host "Kapatiliyor..."
  Stop-Children
  Get-EventSubscriber -ErrorAction SilentlyContinue | ForEach-Object {
    Unregister-Event -SourceIdentifier $_.SourceIdentifier -Force -ErrorAction SilentlyContinue
  }
  Write-Host "Kapandi."
}
