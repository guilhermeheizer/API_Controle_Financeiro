from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from Utilities.auth import decode_access_token


bearer_scheme = HTTPBearer()  # Esquema de autenticação HTTP Bearer para extrair o token do cabeçalho Authorization
bearer_scheme_optinal = HTTPBearer(auto_error=False)  # Esquema opcional para permitir acesso sem token, se necessário

# Função para obter as informações do usuário a partir do token de acesso
def get_current_clains(creaadential: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Aqui você pode implementar a lógica para decodificar o token e obter as informações do usuário
    # Por exemplo, usando a função decode_access_token que você deve ter implementado
    try:
        token = creaadential.credentials
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Token inválido ou expirado.",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload  # ou retorne um objeto de usuário completo se necessário
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido: " + str(e))
    
def get_current_clains_optinal(creaadential: HTTPAuthorizationCredentials = Depends(bearer_scheme_optinal)):
    # Aqui você pode implementar a lógica para decodificar o token e obter as informações do usuário
    # Por exemplo, usando a função decode_access_token que você deve ter implementado
    try:
        if creaadential is None:
            return None  # Retorna None se não houver credenciais, permitindo acesso sem token
        
        token = creaadential.credentials
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Token inválido ou expirado.",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload  # ou retorne um objeto de usuário completo se necessário
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido: " + str(e))