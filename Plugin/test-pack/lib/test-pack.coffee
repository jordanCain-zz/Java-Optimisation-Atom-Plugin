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
      @modalPanel.hide()
    else
      console.log 'Attempting to run some python'
      command = 'C:\\Users\\jordan\\Documents\\GitHub\\javaParser\\runnable.py'
      args = [' ']
      stdout = @stdoutFunc
      exit = (code) -> console.log("Code magically works!!!! #{code}")
      process = new BufferedProcess({command, args, stdout, exit})
      @modalPanel.show()

  stdoutFunc: (output) =>
    console.log("stdoutfunc")
    #output = "test"
    console.log(output)
    output = "test"
    @testPackView.setOutput("output should be here :/")
    #@testPackView.setOutput(output)
