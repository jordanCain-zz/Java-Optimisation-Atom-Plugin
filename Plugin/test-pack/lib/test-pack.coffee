TestPackView = require './test-pack-view'
{CompositeDisposable} = require 'atom'
{BufferedProcess} = require 'atom'

module.exports = TestPack =
  testPackView: null
  modalPanel: null
  subscriptions: null

  activate: (state) ->
    @testPackView = new TestPackView(state.testPackViewState)
    @modalPanel = atom.workspace.addModalPanel(item: @testPackView.getElement(), visible: false)

    # Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    @subscriptions = new CompositeDisposable

    # Register command that toggles this view
    @subscriptions.add atom.commands.add 'atom-workspace', 'test-pack:toggle': => @toggle()

  deactivate: ->
    @modalPanel.destroy()
    @subscriptions.dispose()
    @testPackView.destroy()

  serialize: ->
    testPackViewState: @testPackView.serialize()

  toggle: ->
    if @modalPanel.isVisible()
      @element = @testPackView.getElement()
      while @element.hasChildNodes()
        @element.removeChild(@element.firstChild);
      @modalPanel.hide()
    else
      console.log 'Attempting to run some python'
      editor = atom.workspace.getActiveTextEditor()
      filePath = editor.getPath()
      command = 'C:\\Users\\jordan\\Documents\\GitHub\\javaParser\\runnable.py'
      args = [filePath]
      stdout = (output) => @stdoutFunc output
      exit = (code) -> console.log("Code magically works!!!! #{code}")
      @process = new BufferedProcess({command, args, stdout, exit})
      @modalPanel.show()

#SOURCE:: https://github.com/bleikamp/processing/blob/master/lib/processing-view.coffee
  stdoutFunc: (output) ->
    @testPackView.log(output)
    atom.clipboard.write(output)
