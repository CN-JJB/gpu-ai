Write-Output "=== listener inventory (read-only) ==="
Get-Date
Write-Output ""
Write-Output "--- Get-NetTCPConnection -State Listen ---"
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress,LocalPort,OwningProcess |
  Sort-Object LocalPort |
  Format-Table -AutoSize
Write-Output ""
Write-Output "No firewall/router/NAT setting was changed."
Write-Output "Do not paste secrets or raw Authorization headers into Evidence."
