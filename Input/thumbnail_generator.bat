set blenderPath=%~dp0..\Blender\blender.exe

set renderScript=%~dp0..\Blender\2.80\scripts\addons\automatic_renderer\renderScript.py

set studioPath=%~dp0..\Blender\2.80\scripts\addons\automatic_renderer\Resources\Render_Studio.obj

set HDRIPath=%~dp0..\Blender\2.80\scripts\addons\automatic_renderer\Resources\HDRI_Render.exr

set name=%~n1

mkdir %1\..\..\Output\%name%

set inputPath=%1

set inputFolder=%~dp0..\Input

set outputPath=%1\..\..\Output\%name%

REM for now I'm assuming the objets will be either in glb or gltf
if exist "%inputFolder%\%name%.gltf" goto:gltf
if exist "%inputFolder%\%name%.glb" goto:glb


:gltf
set object_extension=gltf
goto:object_extension_done

:glb
set object_extension=glb
goto:object_extension_done


:object_extension_done
echo object extension is %object_extension%


%blenderPath% -P %renderScript% -- %inputPath% %object_extension% %name% %outputPath% %studioPath% %HDRIPath%
 REM no        1         2       3     4           5              6                  7          8           9            

pause