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
    private var videoIndex = 0
    private var videoPlayerLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            when (result.data?.extras?.get("keyCode")) {
                KeyEvent.KEYCODE_VOLUME_UP -> {
                    // normal modulo -.-
                    videoIndex = ((videoIndex + 1) % videoFiles.size + videoFiles.size) % videoFiles.size
                    launchVideoPlayerActivity()
                }
                KeyEvent.KEYCODE_VOLUME_DOWN -> {
                    videoIndex = ((videoIndex - 1) % videoFiles.size + videoFiles.size) % videoFiles.size
                    launchVideoPlayerActivity()
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        this.videoFiles = File( Environment.getExternalStorageDirectory().path + videoPath).listFiles{ _, filename -> filename.endsWith("mp4")} as Array<File>
        if (this.videoFiles.isEmpty()) {
            Log.d(LOG_TAG, "no videofiles present")
            return
        }
        Log.d(LOG_TAG, videoFiles.size.toString())
        Log.d(LOG_TAG, "aaaaaaaaaaaa")
        launchVideoPlayerActivity()
    }

    private fun launchVideoPlayerActivity() {
        val videoPlayerIntent = Intent(this, VideoPlayerActivity::class.java)
        videoPlayerIntent.putExtra("videoFile", videoFiles[videoIndex])
        videoPlayerLauncher.launch(videoPlayerIntent)
    }
}