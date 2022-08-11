package com.ffxf.holoapp

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.ActivityInfo
import android.media.AudioDescriptor
import android.media.AudioManager
import android.media.MediaPlayer
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.view.WindowInsets
import android.widget.VideoView
import androidx.annotation.RequiresApi
import java.io.File


class VideoPlayerActivity : Activity(), MediaPlayer.OnCompletionListener {
    private lateinit var mVV: VideoView
    private lateinit var audioManager: AudioManager

    @RequiresApi(Build.VERSION_CODES.R)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video_player)

        // change orientation and visibility of navigation-bar
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        window.insetsController?.hide(WindowInsets.Type.navigationBars())

        val videoFile = this.intent.extras?.get("videoFile") as File
        audioManager = getSystemService(Context.AUDIO_SERVICE) as AudioManager
        mVV = findViewById<View>(R.id.videoview) as VideoView
        mVV.setOnCompletionListener(this)
        mVV.setOnPreparedListener { mp -> mp.isLooping = true }
        mVV.setVideoURI(Uri.fromFile(videoFile))
        mVV.start()
    }



    override fun onCompletion(p0: MediaPlayer?) {
        this.finish()
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        setIntent(intent)
        val videoFile = this.intent.extras?.get("videoPath") as File
        mVV.setVideoURI(Uri.fromFile(videoFile))
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent): Boolean {
        if (keyCode == KeyEvent.KEYCODE_POWER ||keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            event.startTracking()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }

    override fun onKeyUp(keyCode: Int, event: KeyEvent): Boolean {
        if (!event.isCanceled) {
            when (keyCode) {
                KeyEvent.KEYCODE_VOLUME_UP -> audioManager.adjustStreamVolume(
                    AudioManager.STREAM_MUSIC,
                    AudioManager.ADJUST_RAISE,
                    AudioManager.FLAG_SHOW_UI
                )
                KeyEvent.KEYCODE_VOLUME_DOWN -> audioManager.adjustStreamVolume(
                    AudioManager.STREAM_MUSIC,
                    AudioManager.ADJUST_LOWER,
                    AudioManager.FLAG_SHOW_UI
                )
            }
        }
        return super.onKeyUp(keyCode, event)
    }

    override fun onKeyLongPress(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_POWER || keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            var keyCodeIntent = Intent()
            keyCodeIntent.putExtra("keyCode", keyCode)
            this.setResult(Activity.RESULT_OK, keyCodeIntent)
            this.finish()
            return true
        }
        return super.onKeyLongPress(keyCode, event)
    }
}