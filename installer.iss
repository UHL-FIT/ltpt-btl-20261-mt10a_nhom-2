[Setup]
; Thông tin chung về ứng dụng
AppName=Real-time Currency Tracker Pro
AppVersion=1.0
AppPublisher=Nhom 2
AppPublisherURL=https://github.com/
AppSupportURL=https://github.com/
AppUpdatesURL=https://github.com/
DefaultDirName={autopf}\CurrencyTrackerPro
DisableProgramGroupPage=yes
; Tên file cài đặt đầu ra
OutputBaseFilename=Setup_CurrencyTrackerPro
; Thêm icon cho file Setup
SetupIconFile=assets\app_icon.ico
; Thư mục lưu file cài đặt (để vào thư mục dist)
OutputDir=dist
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Sao chép tệp thực thi chính (được build từ PyInstaller là main.exe, đổi tên thành CurrencyTrackerPro.exe khi cài đặt)
Source: "dist\main.exe"; DestDir: "{app}"; DestName: "CurrencyTrackerPro.exe"; Flags: ignoreversion
; Sao chép tài liệu hướng dẫn sử dụng
Source: "guide.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "guide.pdf"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('guide.pdf')

[Icons]
; Tạo shortcut ở Start Menu
Name: "{autoprograms}\Real-time Currency Tracker Pro"; Filename: "{app}\CurrencyTrackerPro.exe"
; Tạo shortcut ở Desktop nếu người dùng chọn
Name: "{autodesktop}\Real-time Currency Tracker Pro"; Filename: "{app}\CurrencyTrackerPro.exe"; Tasks: desktopicon

[Run]
; Cho phép chạy ứng dụng ngay sau khi cài đặt xong
Filename: "{app}\CurrencyTrackerPro.exe"; Description: "{cm:LaunchProgram,Real-time Currency Tracker Pro}"; Flags: nowait postinstall skipifsilent
