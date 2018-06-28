Title: Introducing iOS ARKit with "Post Malone Balloon"
Date: 2018-06-24
Category: web, js

![cyberpunk](./cyberpunk/post_1.jpg){:height="300px" width="400px"}

Hi Everyone!

I am starting a series of posts where ***I go deep into AR & VR through fun examples*** and I'd love you to join me!


Today I am going to show how neat is to write an AR iOS application with [ARKit](https://developer.apple.com/arkit/). We are going to dive into a simple but fun [App where you can insert Post Malone balloons](https://github.com/bt3gl/AR_PostMalone) into your reality.

Before everything, I recommend you to watch [WWDC 2017's 'Introducing ARKit: Augmented Reality for iOS'](https://developer.apple.com/videos/play/wwdc2017/602/). It gives a nice overview of ARKit's capabilities.


## The source code for AR_PostMalone the following structure:

## `Info.plist`

An information property list file is a XML file that contains essential configuration information for a bundled executable. Example of the information you want to add is:

* The name of your app (`<string>PostMaloneBalloon</string>`).
* Camera usage (`<key>NSCameraUsageDescription</key>`).
* Frameworks you need (`<key>UIRequiredDeviceCapabilities</key>` with `<string>armv7</string>` and `<string>arkit</string>`).


## `Assets.xcassets` directory

This is where you place assets such as the images used in your App (Post Malone head) and icons. A file `Content.json` is placed inside every directory to describe the assets.

## `Base.lproj` directory

Contains two [story board files](https://www.raywenderlich.com/160521/storyboards-tutorial-ios-11-part-1):

* `LaunchScreen.storyboard`.
* `Main.storyboard`.



## `Scene.swift`

This module is where you call the class `Scene` to control what how the App is operating with the scene. Here we are explicitly using [ARKit](https://developer.apple.com/arkit/) and [SpriteKit](https://developer.apple.com/documentation/spriteKit). Rendering brings tracking and scene understanding together with your content.

For our App, we are:

* Defining the method `touchesBegan`, where we define what happens when we click the scene.
* The sequence of movements is defined by `let sequence = SKAction.sequence([popSound, moveDown, moveDownFloating, moveToBottom])`.
* When you touch the scene, a Post Malone Balloon head appears and starts to behave as a balloon (`moveDownFloating = ((arc4random() % 2)==0) ? moveLeftDown : moveRightDown`).
* The balloon either pops (`let popSound = SKAction.playSoundFileNamed("pop", waitForCompletion: false)`) or fades after a second (`fadeOut = SKAction.fadeOut(withDuration: 1.0)`).


## `ViewController.swift`

The ViewController class inherents from `ARSKViewDelegate` so that we can create a `sceneView` variable. This class has methods for:

* Views
    - Scaling and placing the view.
    - View when it loads (and load the pre-defined scene from [SKScene](https://developer.apple.com/documentation/spritekit/skscene)).
    - View to appear and disappear.
    - Run.

* Sessions
    - Session interrupted.
    - Session ended.



## `AppDelegate.swift`

This is where we call the class `AppDelegate`, which responds for `UIApplicationMain`. In this class we create a variable that will work as the window UI and we have UI methods for:

* See if the application is about to move from active to inactive state (for example, pause ongoing tasks).
* Release shared resources and  save user data.
* Change from the background to the active state.
* Restart any tasks that were paused while the application was inactive.
* Termination actions for when the application is about to terminate (for example, to save data if appropriate).


----

*** Thank you for reading and see you in the next episode! <3***
