Spine = require('spine')

class Search extends Spine.Model
  @configure 'Search', 'name', 'email'
  
  @extend Spine.Model.Local
  
  @filter: (query) ->
    return @all() unless query
    query = query.toLowerCase()
    @select (item) ->
      item.name?.toLowerCase().indexOf(query) isnt -1 or
        item.email?.toLowerCase().indexOf(query) isnt -1
        
module.exports = Search
