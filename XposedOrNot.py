import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def mostrar_banner():
    banner = f"""{Fore.RED}
▗▖  ▗▖▄▄▄▄   ▄▄▄   ▄▄▄ ▗▞▀▚▖   ▐▌ ▗▄▖  ▄▄▄ ▗▖  ▗▖ ▄▄▄     ■  
 ▝▚▞▘ █   █ █   █ ▀▄▄  ▐▛▀▀▘   ▐▌▐▌ ▐▌█    ▐▛▚▖▐▌█   █ ▗▄▟▙▄▖
  ▐▌  █▄▄▄▀ ▀▄▄▄▀ ▄▄▄▀ ▝▚▄▄▖▗▞▀▜▌▐▌ ▐▌█    ▐▌ ▝▜▌▀▄▄▄▀   ▐▌  
▗▞▘▝▚▖█                     ▝▚▄▟▌▝▚▄▞▘     ▐▌  ▐▌        ▐▌  
      ▀                                                  ▐▌  
{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}================ 🔍 Email Breach Checker 📧 ================ \n{Style.RESET_ALL}"""
    print(banner)
    
    spaces = 22
    print(f"{' ' * spaces}{Fore.WHITE}{Style.BRIGHT}By: HackUnderway\n{Style.RESET_ALL}")

def consultar_email_breach(email):
    api_url = f'https://api.xposedornot.com/v1/breach-analytics?email={email}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        mostrar_resultados(data)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✖ Error al conectar con la API: {e}")

def mostrar_resultados(data):
    print(f"\n{Fore.CYAN}🔍 RESULTADOS DE LA CONSULTA{Style.RESET_ALL}")
    
    # Mostrar resumen de riesgo
    risk_info = data.get("BreachMetrics", {}).get("risk", [{}])[0]
    print(f"\n{Fore.YELLOW}⚡ Nivel de riesgo: {Fore.RED if risk_info.get('risk_label') == 'High' else Fore.YELLOW if risk_info.get('risk_label') == 'Medium' else Fore.GREEN}{risk_info.get('risk_label', 'Desconocido')} ({risk_info.get('risk_score', '?')}/100)")
    
    # Mostrar resumen de brechas
    breaches_summary = data.get("BreachesSummary", {}).get("site", "").split(";")
    if breaches_summary and breaches_summary[0]:
        print(f"\n{Fore.YELLOW}📊 Brechas encontradas: {Fore.WHITE}{len(breaches_summary)}")
        print(f"{Fore.YELLOW}🔗 Sitios afectados: {Fore.WHITE}{', '.join(breaches_summary)}")
    else:
        print(f"\n{Fore.GREEN}✅ No se encontraron brechas conocidas para este correo")
    
    # Mostrar métricas por industria
    industry_metrics = data.get("BreachMetrics", {}).get("industry", [[]])[0]
    if industry_metrics:
        print(f"\n{Fore.YELLOW}🏭 Brechas por industria:")
        for industry in industry_metrics:
            if isinstance(industry, list) and len(industry) == 2 and industry[1] > 0:
                print(f"  {Fore.CYAN}{industry[0]}: {Fore.WHITE}{industry[1]} brecha(s)")
    
    # Mostrar detalles de contraseñas
    password_strength = data.get("BreachMetrics", {}).get("passwords_strength", [{}])[0]
    if password_strength:
        print(f"\n{Fore.YELLOW}🔐 Estado de contraseñas expuestas:")
        print(f"  {Fore.RED}Fáciles de crackear: {password_strength.get('EasyToCrack', 0)}")
        print(f"  {Fore.YELLOW}Texto plano: {password_strength.get('PlainText', 0)}")
        print(f"  {Fore.GREEN}Hash fuerte: {password_strength.get('StrongHash', 0)}")
        print(f"  {Fore.BLUE}Desconocido: {password_strength.get('Unknown', 0)}")
    
    # Mostrar detalles de brechas
    exposed_breaches = data.get("ExposedBreaches", {}).get("breaches_details", [])
    if exposed_breaches:
        print(f"\n{Fore.YELLOW}📝 DETALLES DE LAS BRECHAS:{Style.RESET_ALL}")
        for breach in exposed_breaches:
            print(f"\n{Fore.MAGENTA}➤ {breach.get('breach', 'Desconocido')} ({breach.get('industry', '?')})")
            print(f"  {Fore.CYAN}📅 Año: {breach.get('xposed_date', '?')}")
            print(f"  {Fore.CYAN}👤 Registros afectados: {breach.get('xposed_records', '?')}")
            print(f"  {Fore.CYAN}🔓 Datos expuestos: {breach.get('xposed_data', '?')}")
            print(f"  {Fore.CYAN}🔗 Referencia: {breach.get('references', '?')}")
            print(f"  {Fore.CYAN}ℹ️ Detalles: {breach.get('details', '?')[:150]}...")

if __name__ == "__main__":
    mostrar_banner()
    print(f"{Fore.CYAN}🔎 Verificación de brechas de seguridad por email")
    email = input(f"{Fore.WHITE}Ingrese su dirección de correo electrónico: ")
    consultar_email_breach(email)
