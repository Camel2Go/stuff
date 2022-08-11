package com.ffxf.holoapp

import android.content.Intent
import android.os.Bundle
import android.os.Environment
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import java.io.File


class MainActivity : AppCompatActivity() {

    private val TAG: String = MainActivity::class.java.simpleName
    private val videoPath: String = "/Download/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val videoFiles = File( Environment.getExternalStorageDirectory().path + videoPath).listFiles{ _, filename -> filename.endsWith("mp4")}
        if (videoFiles == null || videoFiles.isEmpty()) {
            Log.d(TAG, "No files present")
            return
        }
        playVideo(videoFiles.first())
    }
    private fun playVideo(videoFile: File) {
        val videoPlaybackActivity = Intent(this, VideoPlayerActivity::class.java)
        videoPlaybackActivity.putExtra("videoFile", videoFile)
        startActivity(videoPlaybackActivity)
    }
}