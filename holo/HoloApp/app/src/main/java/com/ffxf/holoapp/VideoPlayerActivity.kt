package com.ffxf.holoapp

import android.app.Activity
import android.content.Intent
import android.content.pm.ActivityInfo
import android.media.MediaPlayer
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.WindowInsets
import android.widget.VideoView
import androidx.annotation.RequiresApi
import java.io.File


class VideoPlayerActivity : Activity(), MediaPlayer.OnCompletionListener {
    private lateinit var mVV: VideoView

    @RequiresApi(Build.VERSION_CODES.R)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video_player)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        window.insetsController?.hide(WindowInsets.Type.navigationBars())
        val videoFile = this.intent.extras?.get("videoFile")
        mVV = findViewById<View>(R.id.videoview) as VideoView
        mVV.setOnCompletionListener(this)
        mVV.setOnPreparedListener { mp -> mp.isLooping = true }
        if (!this.playFile(videoFile as File)) {
            return
        }
        mVV.start()
    }

    private fun playFile(videoFile: File): Boolean {
        if (videoFile.exists() && videoFile.canRead()) {
            mVV.setVideoURI(Uri.fromFile(videoFile))
            return true
        }
        mVV.stopPlayback()
        this.finish()
        return false
    }

    override fun onCompletion(p0: MediaPlayer?) {
        this.finish()
    }
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        setIntent(intent)
        val videoFile = this.intent.extras?.get("videoPath")
        this.playFile(videoFile as File)
    }
}