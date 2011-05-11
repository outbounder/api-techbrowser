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

### search public entries ###
Operation used to search the public data store for entries containing given tags

    GET http://api-techbrowser.appspot.com/search.json?q=plus+delemited+tags

    output: Array of entries : {
                        url:'http://bit.ly/g7H0h2',
                        tags:['technology','genome','project']
                   }


### synch external tags ###
Operation is used to force synching between current techbrowser db instance and the one given by url param. Only new tags will be added and returned as response.

    GET http://localhost:8080/synch.json?url=http://api-techbrowser.appspot.com/tags.json

    output: Array of tag names : string