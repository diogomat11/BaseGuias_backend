from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import BaseGuia, Carteirinha
from typing import Optional
from datetime import date, datetime
import pandas as pd
import io

router = APIRouter(
    prefix="/guias",
    tags=["Guias"]
)

@router.get("/")
def list_guias(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    created_at_start: Optional[date] = None, 
    created_at_end: Optional[date] = None,
    carteirinha_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(BaseGuia)
    
    if created_at_start:
        query = query.filter(BaseGuia.updated_at >= created_at_start)
    if created_at_end:
        query = query.filter(BaseGuia.updated_at <= created_at_end)
    if carteirinha_id:
        query = query.filter(BaseGuia.carteirinha_id == carteirinha_id)

    guias = query.limit(limit).all()
    return guias

@router.get("/export")
def export_guias(
    created_at_start: Optional[str] = Query(None, description="Start Date (YYYY-MM-DD)"),
    created_at_end: Optional[str] = Query(None, description="End Date (YYYY-MM-DD)"),
    carteirinha_id: Optional[int] = Query(None, description="Filter by Carteirinha ID"),
    db: Session = Depends(get_db)
):
    query = db.query(BaseGuia).join(Carteirinha)
    
    if created_at_start:
         query = query.filter(BaseGuia.updated_at >= created_at_start)
    if created_at_end:
         query = query.filter(BaseGuia.updated_at <= str(datetime.strptime(created_at_end, '%Y-%m-%d').date() + pd.Timedelta(days=1)))
    if carteirinha_id:
        query = query.filter(BaseGuia.carteirinha_id == carteirinha_id)

    results = query.all()

    # Format for Excel
    data = []
    for row in results:
        # Helper to format date
        def fmt_date(d):
            return d.strftime("%d/%m/%Y") if d else ""

        data.append({
            "Carteirinha": row.carteirinha_rel.carteirinha,
            "Paciente": row.carteirinha_rel.paciente,
            "Guia": row.guia,
            "Data_Autorização": fmt_date(row.data_autorizacao),
            "Senha": row.senha,
            "Validade": fmt_date(row.validade),
            "Código_Terapia": row.codigo_terapia,
            "Qtde_Solicitada": row.qtde_solicitada,
            "Sessões Autorizadas": row.sessoes_autorizadas,
            "Importado_Em": row.created_at.strftime("%d/%m/%Y %H:%M:%S")
        })

    # Manually creating DF to ensure columns order if list is not empty
    if data:
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Guias')
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="guias_exportadas.xlsx"'
    }
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
