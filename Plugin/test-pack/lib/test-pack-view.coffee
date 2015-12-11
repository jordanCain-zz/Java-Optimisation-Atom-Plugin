module.exports =
class TestPackView

  constructor: (serializedState) ->
    # Create root element
    @element = document.createElement('div')
    @element.classList.add('test-pack')

    # Create message element
    message = document.createElement('div')
    message.textContent = "Test"
    message.classList.add('message')
    @element.appendChild(message)

  getElement: ->
    @element

  log: (output) ->
    console.log(output);
    @element.children[0].textContent = output
