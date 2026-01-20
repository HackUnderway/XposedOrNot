import requests
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
{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}================ 🔍 Email Breach Checker 📧 ================ 
"""
    print(banner)
    print(f"{' ' * 22}{Fore.WHITE}{Style.BRIGHT}By: HackUnderway\n")


def consultar_email_breach(email):
    api_url = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"

    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()
        mostrar_resultados(data)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✖ Error al conectar con la API: {e}")


def mostrar_resultados(data):
    print(f"\n{Fore.CYAN}🔍 RESULTADOS DE LA CONSULTA{Style.RESET_ALL}")

    # 🔴 Caso: email SIN brechas
    if not data or data.get("ExposedBreaches") is None:
        print(f"\n{Fore.GREEN}✅ No se encontraron brechas conocidas para este correo")
        print(f"{Fore.GREEN}🔒 Riesgo estimado: Bajo (0/100)")
        return

    breach_metrics = data.get("BreachMetrics") or {}

    # ===== Riesgo =====
    risk_list = breach_metrics.get("risk") or []
    risk_info = risk_list[0] if risk_list else {}

    risk_label = risk_info.get("risk_label", "Bajo")
    risk_score = risk_info.get("risk_score", 0)

    color = (
        Fore.RED if risk_label == "High"
        else Fore.YELLOW if risk_label == "Medium"
        else Fore.GREEN
    )

    print(f"\n⚡ Nivel de riesgo: {color}{risk_label} ({risk_score}/100)")

    # ===== Resumen de brechas =====
    sites = data.get("BreachesSummary", {}).get("site", "")
    site_list = [s for s in sites.split(";") if s]

    print(f"\n📊 Brechas encontradas: {Fore.WHITE}{len(site_list)}")
    print(f"🔗 Sitios afectados: {Fore.WHITE}{', '.join(site_list)}")

    # ===== Industrias =====
    industry_list = breach_metrics.get("industry") or []
    if industry_list:
        print(f"\n🏭 Brechas por industria:")
        for industry in industry_list[0]:
            if industry[1] > 0:
                print(f"  {Fore.CYAN}{industry[0]}: {Fore.WHITE}{industry[1]} brecha(s)")

    # ===== Contraseñas =====
    passwords = breach_metrics.get("passwords_strength") or []
    if passwords:
        pwd = passwords[0]
        print(f"\n🔐 Estado de contraseñas expuestas:")
        print(f"  {Fore.RED}Fáciles de crackear: {pwd.get('EasyToCrack', 0)}")
        print(f"  {Fore.YELLOW}Texto plano: {pwd.get('PlainText', 0)}")
        print(f"  {Fore.GREEN}Hash fuerte: {pwd.get('StrongHash', 0)}")
        print(f"  {Fore.BLUE}Desconocido: {pwd.get('Unknown', 0)}")

    # ===== Detalles de brechas =====
    breaches = data.get("ExposedBreaches", {}).get("breaches_details", [])
    if breaches:
        print(f"\n📝 DETALLES DE LAS BRECHAS:")
        for breach in breaches:
            print(f"\n{Fore.MAGENTA}➤ {breach.get('breach', 'Desconocido')} ({breach.get('industry', '?')})")
            print(f"  📅 Año: {breach.get('xposed_date', '?')}")
            print(f"  👤 Registros afectados: {breach.get('xposed_records', '?')}")
            print(f"  🔓 Datos expuestos: {breach.get('xposed_data', '?')}")
            print(f"  🔗 Referencia: {breach.get('references', '?')}")
            print(f"  ℹ️ Detalles: {breach.get('details', '')[:1000]}...")


if __name__ == "__main__":
    mostrar_banner()
    print(f"{Fore.CYAN}🔎 Verificación de brechas de seguridad por email")
    email = input(f"{Fore.WHITE}Ingrese su dirección de correo electrónico: ")
    consultar_email_breach(email)
