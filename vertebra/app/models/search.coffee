Spine = require('spine')

class Search extends Spine.Model
  @configure 'Search', 'name', 'synonyms'
  
  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.name?.toLowerCase().indexOf(query) isnt -1
        
module.exports = Search
