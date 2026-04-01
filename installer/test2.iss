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
Source: "DiffSenseAI.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DiffSense AI"; Filename: "{app}\DiffSenseAI.exe"
Name: "{commondesktop}\DiffSense AI"; Filename: "{app}\DiffSenseAI.exe"

[Run]
Filename: "{app}\DiffSenseAI.exe"; Description: "Launch DiffSense AI"; Flags: nowait postinstall skipifsilent

[Code]

var
  LicensePage: TInputQueryWizardPage;
  EmailPage: TInputQueryWizardPage;
  TryButton: TNewButton;
  IsTrialUser: Boolean;
  TrialFile: String;

//////////////////////////////////////////////////////
// 🔥 MACHINE ID (SAFE VERSION)
//////////////////////////////////////////////////////
function GetMachineId(): String;
begin
  Result := GetEnv('COMPUTERNAME');   // 💯 SAFE (no crash)
end;

//////////////////////////////////////////////////////
// 🌐 SERVER VALIDATION (FIXED)
//////////////////////////////////////////////////////
function ValidateLicenseFromServer(key: String): String;
var
  Http: Variant;
  Response: String;
begin
  Result := 'error';

  try
    Http := CreateOleObject('WinHttp.WinHttpRequest.5.1');

    Http.Open('POST', 'https://diffsenseai-ai.onrender.com/api/license/activate', False);
    Http.SetRequestHeader('Content-Type', 'application/json');

    Http.Send('{"LicenseKey":"' + key + '","MachineId":"' + GetMachineId() + '"}');

    Response := LowerCase(String(Http.ResponseText));

    // 🔥 DEBUG (optional)
    // MsgBox(Response, mbInformation, MB_OK);

    if Pos('"status":"activated"', Response) > 0 then
      Result := 'activated'
    else if Pos('"status":"already', Response) > 0 then
      Result := 'used'
    else if Pos('"status":"invalid"', Response) > 0 then
      Result := 'invalid';

  except
    Result := 'error';
  end;
end;

//////////////////////////////////////////////////////
// 🔥 TRY BUTTON
//////////////////////////////////////////////////////
procedure TryFreeClick(Sender: TObject);
begin
  IsTrialUser := True;
  MsgBox('👉 Trial selected. Click Next', mbInformation, MB_OK);
end;

//////////////////////////////////////////////////////
// 📄 CREATE UI
//////////////////////////////////////////////////////
procedure InitializeWizard();
begin
  IsTrialUser := False;

  LicensePage :=
    CreateInputQueryPage(
      wpWelcome,
      'License Activation',
      'Enter your license key',
      'Please enter your license key to continue installation.'
    );

  LicensePage.Add('License Key:', False);

  EmailPage :=
    CreateInputQueryPage(
      LicensePage.ID,
      'Try it free for 15 days',
      'No credit card required',
      'Enter your email and password.'
    );

  EmailPage.Add('Email:', False);
  EmailPage.Add('Password:', True);

  TryButton := TNewButton.Create(WizardForm);
  TryButton.Parent := WizardForm;
  TryButton.Caption := 'Try 15 Days Free';
  TryButton.Left := ScaleX(20);
  TryButton.Top := WizardForm.NextButton.Top;
  TryButton.Width := ScaleX(160);
  TryButton.OnClick := @TryFreeClick;

  TrialFile := ExpandConstant('{localappdata}\DiffSenseAI_trial.txt');
end;

//////////////////////////////////////////////////////
// 💾 SAVE TRIAL (SAFE)
//////////////////////////////////////////////////////
procedure SaveTrial();
begin
  SaveStringToFile(
    TrialFile,
    'STARTED',   // ✅ simple string (NO ERROR EVER)
    False
  );
end;
//////////////////////////////////////////////////////
// 🔐 CHECK TRIAL (NO INT CONVERSION)
//////////////////////////////////////////////////////
function IsTrialValid(): Boolean;
var
  Data: AnsiString;
begin
  Result := True;

  if FileExists(TrialFile) then
  begin
    LoadStringFromFile(TrialFile, Data);

    // simple validation
    if Data <> 'STARTED' then
    begin
      DeleteFile(TrialFile);
      exit;
    end;
  end;
end;

//////////////////////////////////////////////////////
// 🔄 SKIP PAGE
//////////////////////////////////////////////////////
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;

  if (PageID = EmailPage.ID) and (not IsTrialUser) then
    Result := True;
end;

//////////////////////////////////////////////////////
// ✅ MAIN VALIDATION
//////////////////////////////////////////////////////
function NextButtonClick(CurPageID: Integer): Boolean;
var
  email, pass, key, status: String;
begin
  Result := True;

  /////////////////////////////////////////////
  // 🔐 LICENSE FLOW
  /////////////////////////////////////////////
  if CurPageID = LicensePage.ID then
  begin
    key := Trim(LicensePage.Values[0]);

    if (key = '') and (not IsTrialUser) then
    begin
      MsgBox('⚠ Enter License OR click Try Free', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if (key <> '') and (not IsTrialUser) then
    begin
      status := ValidateLicenseFromServer(key);

      if status = 'invalid' then
      begin
        MsgBox('❌ Invalid License', mbError, MB_OK);
        Result := False;
        exit;
      end;

      if status = 'used' then
      begin
        MsgBox('⚠ Already Used', mbError, MB_OK);
        Result := False;
        exit;
      end;

      if status = 'activated' then
        MsgBox('✅ Activated!', mbInformation, MB_OK)
      else
      begin
        MsgBox('❌ Server Error', mbError, MB_OK);
        Result := False;
        exit;
      end;
    end;
  end;

  /////////////////////////////////////////////
  // 📧 TRIAL FLOW
  /////////////////////////////////////////////
  if CurPageID = EmailPage.ID then
  begin
    email := Trim(EmailPage.Values[0]);
    pass := Trim(EmailPage.Values[1]);

    if email = '' then
    begin
      MsgBox('❌ Email required', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if pass = '' then
    begin
      MsgBox('❌ Password required', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if Pos('@', email) = 0 then
    begin
      MsgBox('❌ Invalid Email', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if Length(pass) < 4 then
    begin
      MsgBox('❌ Password too short', mbError, MB_OK);
      Result := False;
      exit;
    end;

    if not IsTrialValid() then
    begin
      Result := False;
      exit;
    end;

    if not FileExists(TrialFile) then
      SaveTrial();

    MsgBox('✅ Trial Started (15 Days)', mbInformation, MB_OK);
  end;
end;