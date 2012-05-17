Spine   = require('spine')
Search = require('models/search')
List    = require('spine/lib/list')
$       = Spine.$

class Sidebar extends Spine.Controller
  className: 'sidebar'
    
  elements:
    '.items': 'items'
    'input': 'finder'
    
  events:
    'keyup input': 'filter'
    'click footer button': 'create'
  
  constructor: ->
    super
    @html require('views/sidebar')()
    
    @list = new List
      el: @items, 
      template: require('views/item'), 
      selectFirst: true

    @list.bind 'change', @change

    @active (params) -> 
      @list.change(Search.find(params.id))
    
    Search.bind('refresh change', @render)
  
  filter: ->
    @query = @finder.val()
    @render()
    
  render: =>
    searches = Search.filter(@query)
    @list.render(searches)
    
  change: (item) =>
    @navigate '/searches', item.id
    
  create: ->
    item = Search.create()
    @navigate('/searches', item.id, 'edit')
    
module.exports = Sidebar
