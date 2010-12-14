# technology browser API node (working title) #
This is unit responsible for providing jsonp or xml based communication with technology browser system.

# Known ui clients #
* http://outbounder.github.com/simplechromeaddon-techbrowser/simplechromeaddon-techbrowser.crx - chrome extension addon, only for adding new links
* http://outbounder.github.com/simpleui-techbrowser/www/index.html - html/js web app, add and search for links by tags

# Known instances #
* http://api-techbrowser.appspot.com/

## Usage/API ##

### request uri structure ####
    http://api-techbrowser.appspot.com/[restURI].jsonp?a1=v1&callback=[jsonpCallback]
    http://api-techbrowser.appspot.com/[restURI].json?a1=v1
  
For clarity following examples will use json request uris

### get tags for url ###
    GET http://api-techbrowser.appspot.com/suggest/tags.json?url=http://bit.ly/g7H0h2
  
    output: Array of items: String
    
### get tag term suggestions ###
    GET http://api-techbrowser.appspot.com/suggest/tag.json?q=term
  
    output: Array of tag suggestions : string

### save url as entry ###
    
    GET http://api-techbrowser.appspot.com/entry.jsonp?url=http://somedomain&tags=plus+delimited+tags&owner=userUUID&source=sourceUUID&callback=methodName
  
    POST http://api-techbrowser.appspot.com/entry.json
      'owner' : "userUUID"
      'source': "sourceUUID"
      'url' : "http://somedomain",
      'tags' : "space delimited tags",

    output: OK or Failed message

*Note that 'owner' and 'source' fields are optional. If the owner value does not exists in the DB it will be created only once.
*Note that when given tag value has been used more than 3 times it gets saved in the tags list used for suggestions.

### search own entries ###
Operation returns not paginated list of submitted entries per owner 

    GET http://api-techbrowser.appspot.com/user/[ownerID]/search.json?q=plus+delemited+tags

    output: Array of entries : {
                        url:'http://bit.ly/g7H0h2',
                        tags:['technology','genome','project']
                   }
                   
Note that 'q' param is optional. if omitted then search operation will return all entries.

### search public entries ###
Operation used to search the public data store for entries containing given tags

    GET http://api-techbrowser.appspot.com/search.json?q=plus+delemited+tags

    output: Array of entries : {
                        url:'http://bit.ly/g7H0h2',
                        tags:['technology','genome','project']
                   }

### subscribe to event stream ###
This operation will result in initiating http post request to given callback once internal unit event is fired.

*Operation not implemented*

    * onNewEntry -> Dispatched when new entry is going to be saved
    * onSearchEntries -> Dispatched when search for entries is executed
    * onNewTag -> Dispatched when new tag is added to auto-suggestion tags list
 
    GET http://api-techbrowser.appspot.com/stream/subscribe/eventName.json?callback=http://myservice.com/handle

### unsubscribe to event ###
This operation will initiate http post request to given callback once internal unit event is fired containing 'eventData'.

*Operation not implemented* 
 
    GET http://api-techbrowser.appspot.com/subscribe/eventName.json?callback=http://myservice.com/handle

## TODO/roadmap & help needed ##
  * upgrade unit & functional tests accordingly to the api
  * add api versioning support
  * provide user data management api or extern to separate unit
