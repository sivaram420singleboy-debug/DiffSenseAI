[Setup]
AppName=DiffSense AI
AppVersion=1.0
AppPublisher=Sivaram
DefaultDirName={autopf}\DiffSenseAI
DefaultGroupName=DiffSense AI
OutputDir=Output
OutputBaseFilename=DiffSenseAI_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\client_app\dist\DiffSenseAI.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DiffSense AI"; Filename: "{app}\DiffSenseAI.exe"
Name: "{commondesktop}\DiffSense AI"; Filename: "{app}\DiffSenseAI.exe"

[Run]
Filename: "{app}\DiffSenseAI.exe"; Description: "Launch DiffSense AI"; Flags: nowait postinstall skipifsilent


[Code]

var
  LicensePage: TInputQueryWizardPage;
  UserLicenseKey: String;  // 🔥 store globally

// ================================
// 🔐 CREATE LICENSE PAGE
// ================================
procedure InitializeWizard();
begin
  LicensePage :=
    CreateInputQueryPage(
      wpWelcome,
      'License Activation',
      'Enter your license key',
      'Please enter your license key to continue installation.'
    );

  LicensePage.Add('License Key:', False);
end;


// ================================
// 🖥 GET MACHINE ID
// ================================
function GetMachineID(): String;
var
  ResultCode: Integer;
  TempFile: String;
  OutputStr: AnsiString;
begin
  TempFile := ExpandConstant('{tmp}\machine.txt');

  Exec(
    'powershell.exe',
    '-Command "(Get-CimInstance Win32_ComputerSystemProduct).UUID | Out-File -Encoding ASCII ''' + TempFile + '''"',
    '',
    SW_HIDE,
    ewWaitUntilTerminated,
    ResultCode
  );

  OutputStr := '';

  if LoadStringFromFile(TempFile, OutputStr) then
    Result := Trim(OutputStr)
  else
    Result := 'UNKNOWN';
end;


// ================================
// 🌐 VALIDATE LICENSE FROM API
// ================================
function ValidateLicense(key: String): Boolean;
var
  ResultCode: Integer;
  URL: String;
  TempFile: String;
  Response: AnsiString;
begin
  URL := 'https://diffsenseai-ai.onrender.com/api/license/activate?LicenseKey='
         + key + '&MachineId=' + GetMachineID();

  TempFile := ExpandConstant('{tmp}\result.txt');

  Result := False;

  if Exec(
    'powershell.exe',
    '-Command "try { (Invoke-WebRequest -Uri ''' + URL + ''' -UseBasicParsing).Content | Out-File -Encoding ASCII ''' + TempFile + ''' } catch { exit 1 }"',
    '',
    SW_HIDE,
    ewWaitUntilTerminated,
    ResultCode
  ) then
  begin
    Response := '';

    if LoadStringFromFile(TempFile, Response) then
    begin
      if (Pos('activated', Response) > 0) or
         (Pos('already_activated', Response) > 0) then
        Result := True;

      if Pos('used_in_other_pc', Response) > 0 then
      begin
        MsgBox('❌ License already used on another PC!', mbError, MB_OK);
        Result := False;
      end;
    end;
  end;
end;


// ================================
// 🚫 BLOCK NEXT IF INVALID
// ================================
function NextButtonClick(CurPageID: Integer): Boolean;
var
  key: String;
begin
  Result := True;

  if CurPageID = LicensePage.ID then
  begin
    key := Trim(LicensePage.Values[0]);

    if key = '' then
    begin
      MsgBox('❌ Please enter license key', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if not ValidateLicense(key) then
    begin
      MsgBox('❌ Invalid or already used license!', mbError, MB_OK);
      Result := False;
      exit;
    end
    else
    begin
      // 🔥 STORE FOR LATER (NOT SAVE HERE)
      UserLicenseKey := key;

      MsgBox('✅ License Activated Successfully!', mbInformation, MB_OK);
    end;
  end;
end;


// ================================
// 📦 AFTER INSTALL COMPLETE → SAVE LICENSE
// ================================
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if UserLicenseKey <> '' then
    begin
      SaveStringToFile(ExpandConstant('{app}\license.txt'), UserLicenseKey, False);
    end;
  end;
end;