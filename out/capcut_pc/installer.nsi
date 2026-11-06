Unicode true
SetCompressor /SOLID lzma
!include "LogicLib.nsh"
!include "nsDialogs.nsh"
!include "MUI2.nsh"

Name "ISUZU NLR - CapCut Project"
OutFile "ISUZU_NLR_CapCut_Setup.exe"
InstallDir "C:\ISUZU_NLR"
RequestExecutionLevel user
ShowInstDetails show

!define SRC "ISUZU_NLR"
Var DRAFT

!define MUI_WELCOMEPAGE_TITLE "ติดตั้งโปรเจกต์ CapCut: ISUZU NLR ทดสอบตู้กันน้ำ"
!define MUI_WELCOMEPAGE_TEXT "ตัวติดตั้งนี้จะ$\r$\n$\r$\n1) วางไฟล์วิดีโอ/เสียงไว้ที่ C:\ISUZU_NLR$\r$\n2) ใส่ 2 โปรเจกต์ลงใน CapCut ให้อัตโนมัติ$\r$\n     • ISUZU_NLR_EditText  (แก้คำได้)$\r$\n     • ISUZU_NLR_FullGraphics  (กราฟิกเต็ม)$\r$\n$\r$\nกรุณาปิด CapCut ก่อนกด ถัดไป"
!define MUI_FINISHPAGE_TITLE "ติดตั้งเสร็จแล้ว"
!define MUI_FINISHPAGE_TEXT "เปิด CapCut แล้วจะเห็นโปรเจกต์ ISUZU_NLR_EditText และ ISUZU_NLR_FullGraphics ในหน้าแรก$\r$\n$\r$\nถ้าขึ้นว่าไฟล์หาย (Media missing) ให้กด Relink แล้วเลือกโฟลเดอร์ C:\ISUZU_NLR\media"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Thai"

Function CheckCapCutClosed
  retry:
    nsExec::ExecToStack 'cmd /c tasklist /FI "IMAGENAME eq CapCut.exe" /NH | find /I "CapCut.exe"'
    Pop $0
    Pop $1
    ${If} $0 == 0
      MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION "CapCut ยังเปิดอยู่$\r$\nกรุณาปิด CapCut ให้หมดก่อน แล้วกด Retry" IDRETRY retry
      Abort
    ${EndIf}
FunctionEnd

Function FindDraftFolder
  StrCpy $DRAFT "$LOCALAPPDATA\CapCut\User Data\Projects\com.lveditor.draft"
  ${IfNot} ${FileExists} "$DRAFT\*.*"
    MessageBox MB_OK|MB_ICONINFORMATION "หาโฟลเดอร์แบบร่างของ CapCut ไม่เจอ$\r$\n$\r$\nเปิด CapCut → ตั้งค่า (Settings) → ดู 'Draft location'$\r$\nแล้วเลือกโฟลเดอร์นั้นในหน้าต่างถัดไป"
    nsDialogs::SelectFolderDialog "เลือกโฟลเดอร์แบบร่าง (Draft location) ของ CapCut" "$LOCALAPPDATA"
    Pop $DRAFT
    ${If} $DRAFT == "error"
    ${OrIf} $DRAFT == ""
      MessageBox MB_OK|MB_ICONSTOP "ยกเลิกการติดตั้ง"
      Abort
    ${EndIf}
  ${EndIf}
FunctionEnd

Section "Install"
  Call CheckCapCutClosed
  Call FindDraftFolder
  DetailPrint "โฟลเดอร์แบบร่าง CapCut: $DRAFT"

  SetOutPath "$INSTDIR\media"
  File /r "${SRC}\media\*.*"
  SetOutPath "$INSTDIR"
  File "${SRC}\README_TH.txt"
  File "${SRC}\sfx_names.txt"
  SetOutPath "$INSTDIR\CapCut_Projects"
  File /r "${SRC}\CapCut_Projects\*.*"

  ; ลบของเก่า (ถ้าเคยติดตั้ง) แล้วใส่ใหม่
  RMDir /r "$DRAFT\ISUZU_NLR_EditText"
  RMDir /r "$DRAFT\ISUZU_NLR_FullGraphics"
  CopyFiles /SILENT "$INSTDIR\CapCut_Projects\ISUZU_NLR_EditText" "$DRAFT"
  CopyFiles /SILENT "$INSTDIR\CapCut_Projects\ISUZU_NLR_FullGraphics" "$DRAFT"
  ${IfNot} ${FileExists} "$DRAFT\ISUZU_NLR_EditText\draft_content.json"
    MessageBox MB_OK|MB_ICONSTOP "คัดลอกโปรเจกต์ลง CapCut ไม่สำเร็จ$\r$\nลอง copy เองจาก C:\ISUZU_NLR\CapCut_Projects ไปที่ $DRAFT"
  ${EndIf}

  FileOpen $0 "$INSTDIR\draft_location.txt" w
  FileWrite $0 "$DRAFT"
  FileClose $0
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  FileOpen $0 "$INSTDIR\draft_location.txt" r
  FileRead $0 $DRAFT
  FileClose $0
  ${If} $DRAFT != ""
    RMDir /r "$DRAFT\ISUZU_NLR_EditText"
    RMDir /r "$DRAFT\ISUZU_NLR_FullGraphics"
  ${EndIf}
  RMDir /r "$INSTDIR"
SectionEnd
