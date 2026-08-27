param(
  [string]$OutDir = "evidence-hardware"
)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Get-Date | Out-File "$OutDir/date.txt"
Get-CimInstance Win32_VideoController |
  Select-Object Name,PNPDeviceID,AdapterRAM,DriverVersion,VideoModeDescription |
  Format-List | Out-File "$OutDir/video-controller.txt"

Get-PnpDevice -Class Display -ErrorAction SilentlyContinue |
  Format-List Status,Class,FriendlyName,InstanceId |
  Out-File "$OutDir/pnp-display.txt"

if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
  nvidia-smi -L | Out-File "$OutDir/nvidia-smi-L.txt"
  nvidia-smi -q | Out-File "$OutDir/nvidia-smi-q.txt"
} else {
  "nvidia-smi unavailable" | Out-File "$OutDir/nvidia-smi-unavailable.txt"
}

if (Get-Command amd-smi -ErrorAction SilentlyContinue) {
  amd-smi version | Out-File "$OutDir/amd-smi-version.txt"
  amd-smi list | Out-File "$OutDir/amd-smi-list.txt"
  amd-smi static | Out-File "$OutDir/amd-smi-static.txt"
  amd-smi metric --pcie | Out-File "$OutDir/amd-smi-pcie.txt"
  amd-smi metric --ecc | Out-File "$OutDir/amd-smi-ecc.txt"
  amd-smi bad-pages | Out-File "$OutDir/amd-smi-bad-pages.txt"
} else {
  "amd-smi unavailable" | Out-File "$OutDir/amd-smi-unavailable.txt"
}

@"
Read-only collection only.
No firmware flash, OC/UV, power/fan changes, error injection or destructive VRAM stress performed.
Unsupported telemetry is UNKNOWN/N/A, not zero.
"@ | Out-File "$OutDir/collector-note.txt"

Write-Output "wrote $OutDir"
