import './App.css';
import Header from './Components/Header';
import NotesListPage from './Pages/NotesListPage';
import NotePage from './Pages/NotePage';
import {HashRouter as Router , Route , Routes} from "react-router-dom"

function App() {
  return (
      <Router>
        <div className="container dark">
          <div className='app'>
            <Header />
            <Routes>
              <Route path='*' exact element={<NotesListPage/>}/>
              <Route path='note/:id' element={<NotePage />}/>
            </Routes>
          </div>
        </div>
      </Router>
  );
}

export default App;
