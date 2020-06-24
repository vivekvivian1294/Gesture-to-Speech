package furhatos.app.videoskill.flow

import furhatos.records.User //Import User records

class OrderData (

)
/* We add an extension variable 'order' to the User model of type OrderData*/
val User. order : OrderData
    get() = data .getOrPut(OrderData::class. qualifiedName , OrderData())