import React, { useState, useEffect } from 'react'
import ListItem from '../Components/ListItem'
import AddButton from '../Components/AddButton'
const NotesListPage = () => {

    const [notes, SetNotes] = useState([])

    useEffect(() => {
        getNotes()
    }, [])

    const getNotes = async () => {
        let response = await fetch('/api/notes/')
        let data = await response.json()
        SetNotes(data)
    }
    
    return (
        <div className='notes'>
            <div className='notes-header'>
                <h2 className='notes-title'>&#9782; Notes</h2>
                <p className='notes-count'>{notes.length}</p>
            </div>
            <div className='notes-list'>
                {notes.map((note, index) => (
                    <>
                        <ListItem index={index} note={note} />
                    </>
                ))}
            </div>
            <AddButton />
        </div>
    )
}

export default NotesListPage
