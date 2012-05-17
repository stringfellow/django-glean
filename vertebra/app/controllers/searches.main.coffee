Spine   = require('spine')
Search = require('models/search')
$       = Spine.$

class Show extends Spine.Controller
  className: 'show'
  
  events:
    'click .edit': 'edit'
  
  constructor: ->
    super
    @active @change
  
  render: ->
    @html require('views/show')(@item)
    
  change: (params) =>
    @item = Search.find(params.id)
    @render()
    
  edit: ->
    @navigate('/searches', @item.id, 'edit')

class Edit extends Spine.Controller
  className: 'edit'
  
  events:
    'submit form': 'submit'
    'click .save': 'submit'
    'click .delete': 'delete'
    
  elements: 
    'form': 'form'
    
  constructor: ->
    super
    @active @change
  
  render: ->
    form_data =
      item: @item
      csrf_token: Search.csrf_token
    @html require('views/form')(form_data)
    
  change: (params) =>
    @item = Search.find(params.id)
    @render()
    
  submit: (e) ->
    e.preventDefault()
    @item.fromForm(@form).save()
    @navigate('/searches', @item.id)
    
  delete: ->
    @item.destroy() if confirm('Are you sure?')
    
class Main extends Spine.Stack
  className: 'main stack'
    
  controllers:
    show: Show
    edit: Edit
    
module.exports = Main
