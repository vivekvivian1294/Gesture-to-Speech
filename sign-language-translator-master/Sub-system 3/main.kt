package furhatos.app.videoskill

import furhatos.app.videoskill.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class VideoskillSkill : Skill() {
    override fun start() {
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
