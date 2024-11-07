import React , {useState , useEffect} from 'react'
import {  useNavigate, useParams } from 'react-router-dom'
import { ReactComponent as ArrowLeft } from  '../assets/arrow-left.svg'

const NotePage = () => {

    let { id } = useParams();
    let [note , setNote ]   = useState(null);
    const navigate = useNavigate();

    useEffect (()=> {
        getNote()
})

    const getNote = async () => {
        if ( id === 'new') return
        
        let response = await fetch (`/api/note/${id}/`)
        let data = await response.json()
        setNote(data);

    }
    const createNote = async () =>{
        fetch(`/api/note/new/`, {
        method : "POST",
        headers : {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(note)
    })
}
    const updateNote = async () =>{
        fetch(`/api/note/${id}/update/`, {
        method : "PUT",
        headers : {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(note)
    })
    }
    const deleteNote = async () =>{
        fetch(`/api/note/${id}/delete/` ,{
            method : "DELETE", 
            headers:{
                'Content-Type': 'application/json'
            }
        })
        navigate('/')
    }
    const handleSubmit = async () =>{
        if (id !== 'new' &&  note.body === " ") {
            deleteNote()
        }else if (id !== 'new'){
            updateNote()
        }else if (id === 'new' && note.body !== null){
            createNote()
        }
        // await  updateNote()
        // console.log(updateNote);
        navigate('/')
    }

    let handleChange = async (value) => {
            setNote(note => ({...note, "body":value}))
    }

  return (
    <div className="note"> 
        <div className='note-header'>
            <h3>    
                
                <ArrowLeft onClick={handleSubmit} />
                {/* <button onClick={deleteNote}>Delete</button> */}
            </h3>
            { id !== 'new' ? (
                <button onClick={deleteNote}>Delete</button>
            ) : (
                <button onClick={(handleSubmit)}> Done</button>
            )}
        </div>
        <div className='note-list-item'>
            <h1>Enter title here :{note?.title}</h1>
            <textarea onChange={(e)=> {handleChange(e.target.value)}} value={note?.body}></textarea>
        </div>
    </div>
  )
}

export default NotePage
