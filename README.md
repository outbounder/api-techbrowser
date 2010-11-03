# technology browser API node (working title) #
This is unit responsible for providing jsonp or xml based communication with technology browser system.

## Usage/API ##

#### General operation format #####
### example(jsonp) ###
 GET/UPDATE/DELETE http://api-techbrowser.appspot.com/<restURI>.jsonp?<arguments>&callback#<callback>
### example(json) ###
  POST/GET/UPDATE/DELETE http://api-techbrowser.appspot.com/<restURI>.json?<arguments>
### example(xml) ###
  POST/GET/UPDATE/DELETE http://api-techbrowser.appspot.com/<restURI>.json?<arguments>
  
  
#### own technologies ####
Operation for list own inputed technologies
### example ###
  GET http://api-techbrowser.appspot.com/own.<format>

-----

  output: Array of techs (Arrays of key-value pairs)

#### auto-tags generation ####
Operation for generating tags per given url (technology). Initially uses predefined content parser and tags matching algorithm.
### example ###
  GET http://api-techbrowser.appspot.com/suggest/tags.<format>?url#<url>

-----

  output: array of strings (tags)

#### save ####
Operation for adding or updating a technology to the data store.

### example ###
  GET http://api-techbrowser.appspot.com/entry.<jsonp>?url=http://somedomain&tags=space+delimited+tags%2fkeywords&owner=someString&callback=methodName
  POST http://api-techbrowser.appspot.com/entry.<xml|json>
  body: 
    data: JSON encoded Array with key-value pairs
      example:
      {
         url: "http://somedomain",
         tags: "space delimited tags/keywords",
		 owner: "someString"
      }
    user: userUID (facebookID, twitterID or gmailID)

  
  Note that owner field is the only optional. If the owner value is not presented as author in the DB it will be created on first add. 
-----

  output: OK or Failed message

#### search ####
Operation used to search the data store for given query.
### example ###
  GET http://api-techbrowser.appspot.com/search.<format>?q#<query>&max#<number>&offset#<number>

-----

  output: Array of techs (Arrays of key-value pairs)
  

#### listSearchSuggestions ####
Operation used to return suggestions for given search query
### example ##
  GET http://api-techbrowser.appspot.com/suggest/search.<format>?q#<query>&max#<number>

-----

  output: Array of search suggestions queries(plain strings)

#### listTagsNamesSuggestions ####
Similar operation to the listSearchSuggestions but instead of givin suggestion for searching, lists suggestions for particular tags values. Output is the same format.

### example ###
  GET http://api-techbrowser.appspot.com/suggest/tag.<format>?q#<query>&max#<number>


## TODO/roadmap & help needed ##
* Update readme to reflect latest operations
* Update json support with validation preventing javascript injection
* Save operation also should take "tags" field value and include every tag which is not listed in "known tags" on every 3rd same user input.
* Provide support for custom url parsing via external units using the "Unit Messaging" spec proposal (http://activebot.net/wiki/abn/spec)
* Provide support for custom storage via external units using the same "Unit Messaging" spec
