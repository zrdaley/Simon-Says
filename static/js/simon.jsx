var moves = []
var simons_moves = []

var moves_dictionary = {
    "#top-left": 1,
    "#top-right": 2,
    "#bottom-left": 3,
    "#bottom-right": 4, 
}

var rev_moves_dictionary = {
    1: "#top-left",
    2: "#top-right",
    3: "#bottom-left",
    4: "#bottom-right", 
}

$(document).ready(function () {
  ReactDOM.render(<Timer />, document.getElementById('container'))
  $('#top-left').click(function(){ click('#top-left', false, 50)})
  $('#top-right').click(function(){ click('#top-right', false, 50)})
  $('#bottom-left').click(function(){ click('#bottom-left', false, 50)})
  $('#bottom-right').click(function(){ click('#bottom-right', false, 50)})
})

function loss(){
  ReactDOM.unmountComponentAtNode(document.getElementById('container'))
  simons_moves = []
  moves = []
  var retry = $('<button id="retry">LOSS. TRY AGAIN?</button>')
  retry.click(function () {
        ReactDOM.render(<Timer />, document.getElementById('container'))
  })
  $("#container").html(retry)
}

function mockMoves(moves, index=0) {
  clickResponse(rev_moves_dictionary[moves[index]], 100)
    setTimeout(function() {
      if (moves.length !== 0 && moves[index + 1] != undefined) {
        mockMoves(moves, index+1)
      }
    }, 400)
}

function click(id, responseTime){
  clickResponse(id, responseTime)
  moves.push(moves_dictionary[id])
  axios.post('/check-move', {moves: moves, simons_moves: simons_moves})
      .then(res => {
        if (!res.data.valid){
          loss()
        }
        else if(moves.length == simons_moves.length){
          moves = []
          ReactDOM.unmountComponentAtNode(document.getElementById('container'))
          ReactDOM.render(<Timer />, document.getElementById('container'))
        }
      })
}

function clickResponse(id, timeout){
  var originalColour = $(id).css('fill')
  $(id).css('fill', 'grey')
  setTimeout(function() {
      $(id).css('fill', originalColour)
    }, timeout)
}

class Timer extends React.Component {
  constructor(props) {
    super(props)
    axios.post('/get-move', {moves: simons_moves})
        .then(res => {
          simons_moves = res.data
          setTimeout(function() {
            mockMoves(res.data)
          }, 600)
        })
    this.state = {secondsElapsed: 30}
  }

  tick() {
    this.setState((prevState) => ({
        secondsElapsed: prevState.secondsElapsed - 1
    }))
  }

  componentDidMount() {
      this.interval = setInterval(() => this.tick(), 1000)
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  render() {
    if(this.state.secondsElapsed < 0){
      axios.post('/check-move', {moves: moves, simons_moves: simons_moves, timeout: true})
        .then(res => {
          if (!res.data.valid){
            loss()
          } else {
            axios.post('/get-move', {moves: simons_moves})
              .then(res => {
                this.state.secondsElapsed = 30
                simons_moves = res.data
                setTimeout(function() {
                  mockMoves(res.data)
                }, 600)
              })
          }
        })
    }
    return (
        <div className="timer">{this.state.secondsElapsed}</div>
    )
  }
}