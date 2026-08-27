param(
  [int]$TargetPid = 0,
  [string]$OutFile = "windows-memory-snapshot.json"
)

$os = Get-CimInstance Win32_OperatingSystem
$page = Get-CimInstance Win32_PageFileUsage

$result = [ordered]@{
  Timestamp = (Get-Date).ToString("o")
  TotalVisibleMemorySizeKB = $os.TotalVisibleMemorySize
  FreePhysicalMemoryKB = $os.FreePhysicalMemory
  TotalVirtualMemorySizeKB = $os.TotalVirtualMemorySize
  FreeVirtualMemoryKB = $os.FreeVirtualMemory
  PageFiles = $page
  TargetProcess = $null
  Note = "Read-only snapshot. Windows concepts/counters are not identical to Linux MemAvailable."
}

if ($TargetPid -gt 0) {
  try {
    $p = Get-Process -Id $TargetPid -ErrorAction Stop
    $result.TargetProcess = [ordered]@{
      Id = $p.Id
      ProcessName = $p.ProcessName
      WorkingSet64 = $p.WorkingSet64
      PrivateMemorySize64 = $p.PrivateMemorySize64
      VirtualMemorySize64 = $p.VirtualMemorySize64
    }
  } catch {
    $result.TargetProcess = "UNAVAILABLE: $($_.Exception.Message)"
  }
}

$result | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $OutFile
$result | ConvertTo-Json -Depth 6
Write-Output "No memory stress or system setting changes were performed."
