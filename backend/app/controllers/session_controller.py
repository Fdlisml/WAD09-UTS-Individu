from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from app.data import shuttle_sessions
from app.models.session import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_next_id():
    if not shuttle_sessions:
        return 1
    return max(session["id"] for session in shuttle_sessions) + 1

@router.get("", response_model=dict)
def get_sessions(
    q: Optional[str] = Query(None, description="Search by passenger name or route"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Items per page")
):
    results = shuttle_sessions
    
    # Search
    if q:
        q_lower = q.lower()
        results = [
            s for s in results 
            if q_lower in s["passenger_name"].lower() or q_lower in s["route"].lower()
        ]
        
    # Pagination
    total = len(results)
    start = (page - 1) * limit
    end = start + limit
    paginated_results = results[start:end]
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": paginated_results
    }

@router.get("/{id}", response_model=SessionResponse)
def get_session(id: int):
    for session in shuttle_sessions:
        if session["id"] == id:
            return session
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionCreate):
    new_session = session.dict()
    new_session["id"] = get_next_id()
    shuttle_sessions.append(new_session)
    return new_session

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(id: int):
    for i, session in enumerate(shuttle_sessions):
        if session["id"] == id:
            del shuttle_sessions[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
