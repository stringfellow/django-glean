Spine = require('spine')

class Search extends Spine.Model
  @configure 'Search', 'term', 'synonyms'
  
module.exports = Search
