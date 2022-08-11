package com.ffxf.holoapp

import android.content.Intent
import android.os.Bundle
import android.os.Environment
import android.os.PowerManager
import android.util.Log
import android.view.KeyEvent
import androidx.appcompat.app.AppCompatActivity
import java.io.File


class MainActivity : AppCompatActivity() {

    private val LOG_TAG: String = MainActivity::class.java.simpleName
    private val videoPath: String = "/Download/"
    private var videoFiles: Array<File> = emptyArray()
    private var videoIndex = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        videoFiles = File( Environment.getExternalStorageDirectory().path + videoPath).listFiles{ _, filename -> filename.endsWith("mp4")}
        if (videoFiles.isEmpty()) {
            Log.d(LOG_TAG, "no videofiles present")
            return
        }
        playVideo()
    }
    private fun playVideo() {
        val videoPlaybackActivity = Intent(this, VideoPlayerActivity::class.java)
        videoPlaybackActivity.putExtra("videoFile", videoFiles.get(videoIndex))
        startActivity(videoPlaybackActivity)
    }

    override fun onKeyLongPress(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_POWER) {
            startActivity(Intent("android.intent.action.ACTION_REQUEST_SHUTDOWN"));
            // PowerManagerService.shutdown()
            // This only works for system applications (signed with phone vendor key) with special permissions
            return true
        } else if (keyCode == KeyEvent.KEYCODE_VOLUME_UP) {
            videoIndex++
            playVideo()
            return true
        } else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            videoIndex--
            playVideo()
            return true
        }
        return super.onKeyLongPress(keyCode, event)
    }
}