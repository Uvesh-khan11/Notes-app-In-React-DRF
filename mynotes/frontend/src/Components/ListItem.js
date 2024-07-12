import React from 'react'
import { Link } from 'react-router-dom'

let getTime = (note) =>{
  return new Date(note.updated).toLocaleDateString()
}
const ListItem = ({note , index}) => {
  return (
    // <div key={index}>
    //   <h1>{note.title}</h1>
    //   <h3>{note.body}</h3>
    // </div>
    <Link to={`/note/${note.id}`}>
      <div className='notes-list-item'>
        <h1>{note.title}</h1>
        <p><span>{getTime(note)}</span></p>
      </div>
    </Link>
    
  )
}

export default ListItem
