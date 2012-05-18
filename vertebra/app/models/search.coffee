Spine = require('spine')

class Search extends Spine.Model
  @configure 'Search', 'term', 'synonyms', 'user'

  @extend Spine.Model.Ajax
  
  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.term?.toLowerCase().indexOf(query) isnt -1
        
module.exports = Search
