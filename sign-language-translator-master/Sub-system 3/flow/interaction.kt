package furhatos.app.videoskill.flow

import furhatos.app.videoskill.flow.Greetings
import furhatos.app.videoskill.nlu.*
import furhatos.flow.kotlin.*
import furhatos.gestures.Gestures
import furhatos.nlu.common.Yes
import java.util.*



val Start : State = state(Greetings) {

    onEntry {
        furhat.ask("Hi, are you here for the sign language detection?")
    }

    onResponse<Yes>{
        furhat.say("Welcome")
        //      furhat.ask("Do you want the sign detection by voice or gesture input")
        maint()
        furhat .gesture(Gestures.Smile( duration= 2.0 , strength = 1.0 ))
    }

    onResponse<RegisterVoice>{
        furhat.say("Kindly talk")
        furhat .gesture(Gestures.Smile( duration= 2.0 , strength = 1.0 ))
        goto( HandGesture )

    }

    onResponse<RegisterGesture>{
        furhat.say("Enter Gesture")
        furhat .gesture(Gestures.Smile( duration= 2.0 , strength = 1.0 ))
        maint()
    }

}

fun FlowControlRunner.maint() {

    val number1 = Scanner(System.`in`)
    print("Enter an integer: ")

    var Index: Int = number1.nextInt()
    var temp = Index
    delay(4000)
    print("Enter an integer: ")

    var Index2 = number1.nextInt()
    if (Index2 == Index){
        if (Index == 0)
        {
            furhat.say("This is A")
            maint()
        }
        else if (Index == 1)
        {
            furhat.say("This is B")
            maint()
        }
        else  if (Index == 2)
        {
            furhat.say("This is C")
            maint()
        }
        else if (Index == 3)
        {
            furhat.say("This is D")
            maint()
        }
        else if (Index == 4)
        {
            furhat.say("This is E")
            maint()
        }
        else if (Index == 5)
        {
            furhat.say("This is F")
            maint()
        }

    }
    else
    {
        if (Index == 0 && Index2 == 1){
            furhat.say("This is G")
            maint()
        }
        else if (Index == 0 && Index2 == 2){
            furhat.say("This is H")
            maint()
        }
        else if (Index == 0 && Index2 == 3){
            furhat.say("This is I")
            maint()
        }
        else if (Index == 0 && Index2 == 4){
            furhat.say("This is J")
            maint()
        }
        else if (Index == 0 && Index2 == 5){
            furhat.say("This is K")
            maint()
        }
    }

}

val HandGesture = state(Greetings) {
    onEntry {
        furhat.ask( "What kind of gestures do you want to show?" )
    }

    onResponse<RegisterGestureA> {
        furhat.say("This is A")
        furhat.ask("Which other gesture do you want to show?")
    }

    onResponse<RegisterGestureB> {
        furhat.say("This is B")
        furhat.ask("Which other gesture do you want to show?")
    }

    onResponse<RegisterGestureC> {
        furhat.say("This is C")
        furhat.ask("Which other gesture do you want to show?")
    }

    onResponse<RegisterGestureD> {
        furhat.say("This is D")
        furhat.ask("Which other gesture do you want to show?")
    }

    onResponse<RegisterGestureE> {
        furhat.say("This is E")
        furhat.ask("Which other gesture do you want to show?")
    }

    onResponse<RegisterGestureF> {
        furhat.say("This is F")
        furhat.ask("Which other gesture do you want to show?")
    }
}