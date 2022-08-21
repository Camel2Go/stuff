#!/bin/bash
# https://stackoverflow.com/questions/28302833/how-to-install-an-app-in-system-app-while-developing-from-android-studio

# CHANGE THESE FOR YOUR APP
app_package="com.ffxf"
dir_app_name="holoapp"
MAIN_ACTIVITY="holoapp.MainActivity"

ADB="adb" # how you execute adb
ADB_SH="$ADB shell su -c"

path_sysapp="/system/priv-app" # assuming the app is priviledged
apk_host="./app/build/outputs/apk/debug/app-debug.apk"
apk_name=$dir_app_name".apk"
apk_target_dir="$path_sysapp/$dir_app_name"
apk_target_sys="$apk_target_dir/$apk_name"

echo -n "remounting system as read/write..."
$ADB_SH "mount -o rw,remount /system"
echo "done!"

# $ADB_SH "chmod 777 /system/lib/"
echo "pushing app to device..."
$ADB_SH "mkdir -p $apk_target_dir"
$ADB push $apk_host /sdcard/tmp/$apk_name
echo "done!"

echo -n "moving app to priv-app..."
$ADB_SH "mv /sdcard/tmp/$apk_name $apk_target_sys"
# $ADB_SH "pm install -r $apk_target_sys"
echo "done!"

# Give permissions
echo -n "setting permissions..."
$ADB_SH "chmod 755 $apk_target_dir"
$ADB_SH "chmod 644 $apk_target_sys"
echo "done!"

#Unmount system
echo -n "remounting system as read only..."
$ADB_SH "mount -o remount,ro /"
echo "done!"

# Stop the app
# $ADB shell "am force-stop $app_package"

# Re execute the app
# $ADB shell "am start -n \"$app_package.$dir_app_name/$app_package.$MAIN_ACTIVITY\" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER"
