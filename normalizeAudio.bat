REM cls
REM echo off
ffmpeg -i %1 -filter_complex "[0:a]loudnorm=I=-15:TP=-1.25:LRA=11:print_format=summary" -f null x 2>%1.txt
@for /f "tokens=3" %%a in ('findstr /C:"Input Integrated" %1.txt') do (set II=%%a)
echo %II% is the Input Integrated
@for /f "tokens=4" %%a in ('findstr /C:"Input True Peak" %1.txt') do (set ITP=%%a)
echo %ITP% is the Input True Peak
@for /f "tokens=3" %%a in ('findstr /C:"Input LRA" %1.txt') do (set ILRA=%%a)
echo %ILRA% is the Input LRA
@for /f "tokens=3" %%a in ('findstr /C:"Input Threshold" %1.txt') do (set IT=%%a)
echo %IT% is the Input Threshold
@for /f "tokens=3" %%a in ('findstr /C:"Output Integrated" %1.txt') do (set OI=%%a)
echo %OI% is the Output Integrated
@for /f "tokens=4" %%a in ('findstr /C:"Output True Peak" %1.txt') do (set OTP=%%a)
echo %OTP% is the Output True Peak
@for /f "tokens=3" %%a in ('findstr /C:"Output LRA" %1.txt') do (set OLRA=%%a)
echo %OLRA% is the Output LRA
@for /f "tokens=3" %%a in ('findstr /C:"Output Threshold" %1.txt') do (set OT=%%a)
echo %OT% is the Output Threshold
@for /f "tokens=3" %%a in ('findstr /C:"Target Offset" %1.txt') do (set TO=%%a)
echo %TO% is the Target Offset


ffmpeg -i %1 -af loudnorm=linear=true:I=-15:LRA=11:tp=-1.25:measured_I=%II%:measured_LRA=%ILRA%:measured_tp=%ITP%:measured_thresh=%IT%:offset=%TO%:print_format=summary normalizedLoudenedOutput.mkv