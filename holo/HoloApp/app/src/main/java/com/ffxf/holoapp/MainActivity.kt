package com.ffxf.holoapp

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.os.Environment
import android.os.PowerManager
import android.util.Log
import android.view.KeyEvent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import java.io.File


class MainActivity : AppCompatActivity() {

    private val LOG_TAG: String = MainActivity::class.java.simpleName
    private val videoPath: String = "/Download/"
    private var videoFiles: Array<File> = emptyArray()
    private var videoIndex = 1
    private var videoPlayerLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            when (result.data?.extras?.get("keyCode")) {
                KeyEvent.KEYCODE_POWER -> {
                    startActivity(Intent("android.intent.action.ACTION_REQUEST_SHUTDOWN"));
                    // PowerManagerService.shutdown()
                    // This only works for system applications (signed with phone vendor key) with special permissions
                }
                KeyEvent.KEYCODE_VOLUME_UP -> {
                    TODO("modulo ändern")
                    videoIndex = (videoIndex + 1) % videoFiles.size
                    playVideo()
                }
                KeyEvent.KEYCODE_VOLUME_DOWN -> {
                    TODO("modulo ändern")
                    videoIndex = (videoIndex - 1) % videoFiles.size
                    playVideo()
                }
            }
        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        this.videoFiles = File( Environment.getExternalStorageDirectory().path + videoPath).listFiles{ _, filename -> filename.endsWith("mp4")}
        if (this.videoFiles.isEmpty()) {
            Log.d(LOG_TAG, "no videofiles present")
            return
        }
        Log.d(LOG_TAG, videoFiles.size.toString())
        playVideo()
    }
    private fun playVideo() {
        val videoPlayerIntent = Intent(this, VideoPlayerActivity::class.java)
        videoPlayerIntent.putExtra("videoFile", videoFiles[videoIndex])
        videoPlayerLauncher.launch(videoPlayerIntent)
    }
}