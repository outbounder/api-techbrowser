# technology browser API node (working title) #
This is unit responsible for providing jsonp or xml based communication with technology browser system.

# Known ui clients #
* http://outbounder.github.com/simplechromeaddon-techbrowser/simplechromeaddon-techbrowser.crx - chrome extension addon, only for adding new links
* http://outbounder.github.com/simpleui-techbrowser/www/index.html - html/js web app, add and search for links by tags

# Known instances #
* http://api-techbrowser.appspot.com/

# Known database endpoints #

## Usage/API ##

### request uri structure ####
    http://api-techbrowser.appspot.com/[restURI].jsonp?a1=v1&callback=[jsonpCallback]
    http://api-techbrowser.appspot.com/[restURI].json?a1=v1
  
For clarity following examples will use json request uris

### get tag suggestions for url ###
Operation for generating tags per given url (an Entry). Initially uses predefined content parser and tags matching algorithm.
#### example ####
    GET http://api-techbrowser.appspot.com/suggest/tags.json?url=http://bit.ly/g7H0h2
  
    output: Array of tagnames : string

### save url as entry ###
Operation for adding or updating a technology to the data store. This operation does several actions behind the scenes:
  * creates owner entry*
  * creates an entry if does not exists (search is based on url)   
  * rates an entry if already exists
  
*Operation in Development*
   
#### example ####
    GET http://api-techbrowser.appspot.com/entry/[name].jsonp?url=http://somedomain&tags=plus+delimited+tags&owner=userUUID&source=sourceUUID&callback=methodName
  
    POST http://api-techbrowser.appspot.com/entry/[name].json
      'owner' : "userUUID"
      'source': "sourceUUID"
      'url' : "http://somedomain",
      'tags' : "space delimited tags"

    output: OK or Failed message

*Note that owner and source fields are _the_ only optional. If the owner value is not presented as author in the DB it will be created on first iteration.

### search own entries ###
Operation returns not paginated list of submitted entries per owner 
#### example ####
    GET http://api-techbrowser.appspot.com/user/[ownerID]/search.json?q=plus+delemited+tags

    output: Array of entries : {
                        url:'http://bit.ly/g7H0h2',
                        tags:['technology','genome','project']
                   }
                   
Note that 'q' param is optional. if omitted then search operation will return all entries

### search public entries ###
Operation used to search the public data store for entries containing given tags
#### example ####
    GET http://api-techbrowser.appspot.com/search.json?q=plus+delemited+tags

    output: Array of entries : {
                        url:'http://bit.ly/g7H0h2',
                        tags:['technology','genome','project']
                   }
  

### get search suggestions ###
Operation used to return suggestions upon current search.
#### example ###
    GET http://api-techbrowser.appspot.com/suggest/search.json?q=term

    output: Array of search suggestions : string


### get tag suggestions ###
Similar operation to the above one but instead of giving suggestion for searching, returns suggestions for particular tags values.
#### example ####
    GET http://api-techbrowser.appspot.com/suggest/tag.json?q=term
  
    output: Array of tag suggestions : string

### subscribe to event stream ###
This operation will result in initiating http post request to given callback once internal unit event is fired.

*Operation in development*
    * onNewEntry -> Dispatched when new entry is going to be saved
    * onSearchEntries -> Dispatched when search for entries is executed
    * onNewTag -> Dispatched when new tag is added to auto-suggestion tags list
 
#### example ####
    GET http://api-techbrowser.appspot.com/stream/subscribe/eventName.json?callback=http://myservice.com/handle

### unsubscribe to event ###
This operation will initiate http post request to given callback once internal unit event is fired containing 'eventData'.

*Operation in development* 
 
#### example ####
    GET http://api-techbrowser.appspot.com/subscribe/eventName.json?callback=http://myservice.com/handle

## TODO/roadmap & help needed ##
  * upgrade unit & functional tests accordingly to the api
  * add api versioning support
  * provide user data management api or extern to separate unit
