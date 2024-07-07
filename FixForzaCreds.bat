@echo off
for /f "tokens=1,2 delims= " %%G in ('cmdkey /list ^| findstr "Xbl"') do (
    cmdkey /delete:%%H
)

net stop VaultSvc
net start VaultSvc