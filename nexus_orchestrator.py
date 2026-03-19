"""
╔═══════════════════════════════════════════════════════════════════════╗
║              NEXUS ORCHESTRATOR — The Invisible Thread                ║
║                                                                       ║
║   "नचिकेतास्त्रिरग्निं संचिकाय..."                                    ║
║   "Nachiketas assembled the fire three times..."                       ║
║                              — Katha Upanishad 1.1.15                 ║
║                                                                       ║
║   Just as fire assembled three times opens the door to immortality,  ║
║   the three layers of this orchestrator open the door to             ║
║   unified cosmic intelligence.                                        ║
║                                                                       ║
║   Layer 1: Spawn all 64 Temple servers                               ║
║   Layer 2: Route queries through the 8 Bhairava hubs                 ║
║   Layer 3: Synthesize through the Gemini Avatar Node (Temple 65)     ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import httpx


# ═══════════════════════════════════════
#  TEMPLE REGISTRY — The 64 + 1 Catalog
# ═══════════════════════════════════════

@dataclass
class Temple:
    number: int
    name: str
    script: str
    bhairava: str
    domain: str
    port: int
    env_key: str = ""
    status: str = "dormant"
    process: Any = field(default=None, repr=False)


TEMPLE_REGISTRY: list[Temple] = [
    # ── Productivity (1-10) ──
    Temple(1,  "Jira",            "jira_mcp_server.py",         "Asitanga",  "productivity", 9001, "JIRA_API_TOKEN"),
    Temple(2,  "GitHub",          "github_mcp_server.py",       "Asitanga",  "productivity", 9002, "GITHUB_TOKEN"),
    Temple(3,  "Slack",           "slack_mcp_server.py",        "Asitanga",  "productivity", 9003, "SLACK_BOT_TOKEN"),
    Temple(4,  "Confluence",      "confluence_mcp_server.py",   "Asitanga",  "productivity", 9004, "CONFLUENCE_API_TOKEN"),
    Temple(5,  "Notion",          "notion_mcp_server.py",       "Asitanga",  "productivity", 9005, "NOTION_API_KEY"),
    Temple(6,  "Gmail",           "gmail_mcp_server.py",        "Ruru",      "productivity", 9006, "GOOGLE_OAUTH_TOKEN"),
    Temple(7,  "GoogleCalendar",  "gcal_mcp_server.py",         "Ruru",      "productivity", 9007, "GOOGLE_OAUTH_TOKEN"),
    Temple(8,  "GoogleDrive",     "gdrive_mcp_server.py",       "Ruru",      "productivity", 9008, "GOOGLE_OAUTH_TOKEN"),
    Temple(9,  "Trello",          "trello_mcp_server.py",       "Asitanga",  "productivity", 9009, "TRELLO_API_KEY"),
    Temple(10, "Asana",           "asana_mcp_server.py",        "Asitanga",  "productivity", 9010, "ASANA_ACCESS_TOKEN"),

    # ── Cloud & DevOps (11-20) ──
    Temple(11, "AWS",             "aws_mcp_server.py",          "Samhara",   "cloud",        9011, "AWS_ACCESS_KEY_ID"),
    Temple(12, "GCP",             "gcp_mcp_server.py",          "Samhara",   "cloud",        9012, "GOOGLE_CLOUD_KEY"),
    Temple(13, "Azure",           "azure_mcp_server.py",        "Samhara",   "cloud",        9013, "AZURE_API_KEY"),
    Temple(14, "Docker",          "docker_mcp_server.py",       "Chanda",    "devops",       9014, ""),
    Temple(15, "Kubernetes",      "k8s_mcp_server.py",          "Chanda",    "devops",       9015, "KUBECONFIG"),
    Temple(16, "Vercel",          "vercel_mcp_server.py",       "Samhara",   "cloud",        9016, "VERCEL_TOKEN"),
    Temple(17, "Netlify",         "netlify_mcp_server.py",      "Samhara",   "cloud",        9017, "NETLIFY_TOKEN"),
    Temple(18, "Cloudflare",      "cloudflare_mcp_server.py",   "Samhara",   "cloud",        9018, "CLOUDFLARE_API_TOKEN"),
    Temple(19, "Heroku",          "heroku_mcp_server.py",       "Samhara",   "cloud",        9019, "HEROKU_API_KEY"),
    Temple(20, "DigitalOcean",    "digitalocean_mcp_server.py", "Samhara",   "cloud",        9020, "DIGITALOCEAN_TOKEN"),

    # ── Data & AI (21-30) ──
    Temple(21, "PostgreSQL",      "postgres_mcp_server.py",     "Chanda",    "data",         9021, "DATABASE_URL"),
    Temple(22, "MongoDB",         "mongodb_mcp_server.py",      "Chanda",    "data",         9022, "MONGODB_URI"),
    Temple(23, "Redis",           "redis_mcp_server.py",        "Chanda",    "data",         9023, "REDIS_URL"),
    Temple(24, "Elasticsearch",   "elastic_mcp_server.py",      "Chanda",    "data",         9024, "ELASTIC_API_KEY"),
    Temple(25, "HuggingFace",     "hf_mcp_server.py",           "Chanda",    "ai",           9025, "HF_TOKEN"),
    Temple(26, "OpenAI",          "openai_mcp_server.py",       "Chanda",    "ai",           9026, "OPENAI_API_KEY"),
    Temple(27, "AnthropicClaude", "anthropic_mcp_server.py",    "Chanda",    "ai",           9027, "ANTHROPIC_API_KEY"),
    Temple(28, "Pinecone",        "pinecone_mcp_server.py",     "Chanda",    "data",         9028, "PINECONE_API_KEY"),
    Temple(29, "Supabase",        "supabase_mcp_server.py",     "Chanda",    "data",         9029, "SUPABASE_KEY"),
    Temple(30, "Firebase",        "firebase_mcp_server.py",     "Chanda",    "data",         9030, "FIREBASE_ADMIN_KEY"),

    # ── Communication (31-40) ──
    Temple(31, "Discord",         "discord_mcp_server.py",      "Ruru",      "comms",        9031, "DISCORD_BOT_TOKEN"),
    Temple(32, "Telegram",        "telegram_mcp_server.py",     "Ruru",      "comms",        9032, "TELEGRAM_BOT_TOKEN"),
    Temple(33, "Twitter_X",       "twitter_mcp_server.py",      "Asitanga",  "comms",        9033, "TWITTER_BEARER_TOKEN"),
    Temple(34, "LinkedIn",        "linkedin_mcp_server.py",     "Asitanga",  "comms",        9034, "LINKEDIN_ACCESS_TOKEN"),
    Temple(35, "WhatsApp",        "whatsapp_mcp_server.py",     "Ruru",      "comms",        9035, "WHATSAPP_TOKEN"),
    Temple(36, "SendGrid",        "sendgrid_mcp_server.py",     "Ruru",      "comms",        9036, "SENDGRID_API_KEY"),
    Temple(37, "Twilio",          "twilio_mcp_server.py",       "Ruru",      "comms",        9037, "TWILIO_AUTH_TOKEN"),
    Temple(38, "Mailchimp",       "mailchimp_mcp_server.py",    "Ruru",      "comms",        9038, "MAILCHIMP_API_KEY"),
    Temple(39, "Zoom",            "zoom_mcp_server.py",         "Ruru",      "comms",        9039, "ZOOM_JWT_TOKEN"),
    Temple(40, "MSTeams",         "teams_mcp_server.py",        "Asitanga",  "comms",        9040, "TEAMS_BOT_TOKEN"),

    # ── Commerce & Finance (41-50) ──
    Temple(41, "Stripe",          "stripe_mcp_server.py",       "Unmatta",   "finance",      9041, "STRIPE_SECRET_KEY"),
    Temple(42, "PayPal",          "paypal_mcp_server.py",       "Unmatta",   "finance",      9042, "PAYPAL_CLIENT_SECRET"),
    Temple(43, "Shopify",         "shopify_mcp_server.py",      "Unmatta",   "commerce",     9043, "SHOPIFY_ACCESS_TOKEN"),
    Temple(44, "WooCommerce",     "woo_mcp_server.py",          "Unmatta",   "commerce",     9044, "WOO_CONSUMER_SECRET"),
    Temple(45, "Binance",         "binance_mcp_server.py",      "Unmatta",   "crypto",       9045, "BINANCE_API_KEY"),
    Temple(46, "CoinGecko",       "coingecko_mcp_server.py",    "Unmatta",   "crypto",       9046, ""),
    Temple(47, "QuickBooks",      "quickbooks_mcp_server.py",   "Unmatta",   "finance",      9047, "QUICKBOOKS_CLIENT_ID"),
    Temple(48, "Airtable",        "airtable_mcp_server.py",     "Asitanga",  "data",         9048, "AIRTABLE_API_KEY"),
    Temple(49, "Salesforce",      "salesforce_mcp_server.py",   "Unmatta",   "crm",          9049, "SALESFORCE_ACCESS_TOKEN"),
    Temple(50, "HubSpot",         "hubspot_mcp_server.py",      "Unmatta",   "crm",          9050, "HUBSPOT_API_KEY"),

    # ── Monitoring & Security (51-60) ──
    Temple(51, "Grafana",         "grafana_mcp_server.py",      "Bhishana",  "monitoring",   9051, "GRAFANA_API_KEY"),
    Temple(52, "Datadog",         "datadog_mcp_server.py",      "Bhishana",  "monitoring",   9052, "DATADOG_API_KEY"),
    Temple(53, "Sentry",          "sentry_mcp_server.py",       "Bhishana",  "monitoring",   9053, "SENTRY_AUTH_TOKEN"),
    Temple(54, "PagerDuty",       "pagerduty_mcp_server.py",    "Bhishana",  "monitoring",   9054, "PAGERDUTY_API_KEY"),
    Temple(55, "Vault",           "vault_mcp_server.py",        "Bhishana",  "security",     9055, "VAULT_TOKEN"),
    Temple(56, "Auth0",           "auth0_mcp_server.py",        "Bhishana",  "security",     9056, "AUTH0_MGMT_TOKEN"),
    Temple(57, "Okta",            "okta_mcp_server.py",         "Bhishana",  "security",     9057, "OKTA_API_TOKEN"),
    Temple(58, "Prometheus",      "prometheus_mcp_server.py",   "Bhishana",  "monitoring",   9058, "PROMETHEUS_URL"),
    Temple(59, "NewRelic",        "newrelic_mcp_server.py",     "Bhishana",  "monitoring",   9059, "NEW_RELIC_API_KEY"),
    Temple(60, "Splunk",          "splunk_mcp_server.py",       "Bhishana",  "monitoring",   9060, "SPLUNK_TOKEN"),

    # ── Sacred (61-64) ──
    Temple(61, "Wikipedia",       "wikipedia_mcp_server.py",    "Bhishana",  "sacred",       9061, ""),
    Temple(62, "RSS_News",        "rss_mcp_server.py",          "Asitanga",  "sacred",       9062, ""),
    Temple(63, "WeatherAPI",      "weather_mcp_server.py",      "Krodhana",  "sacred",       9063, "WEATHER_API_KEY"),
    Temple(64, "NewZyon_KAN",     "newzyon_mcp_server.py",      "Bhishana",  "sacred",       9064, "NEWZYON_API_KEY"),

    # ── The Witness (65) ── Gemini Avatar Node
    Temple(65, "GeminiAvatar",    "gemini_avatar_node.py",      "Mithuna",   "witness",      9065, "GEMINI_API_KEY"),
]

BHAIRAVA_HUBS: dict[str, list[int]] = {}
for t in TEMPLE_REGISTRY:
    BHAIRAVA_HUBS.setdefault(t.bhairava, []).append(t.number)


# ═══════════════════════════════════
#  ORCHESTRATOR — The Sutradhra
# ═══════════════════════════════════

class NexusOrchestrator:
    """
    The Sutradhra (Thread-holder) — holds all 65 temples in awareness simultaneously.
    Named after the Sutradhra in classical Sanskrit drama: the stage manager
    who is present but invisible, who sets everything in motion, who witnesses all.
    """

    def __init__(self):
        self.temples = {t.number: t for t in TEMPLE_REGISTRY}
        self.base_dir = Path(__file__).parent
        self._health_callbacks: list[Callable] = []

    def get_temples_by_bhairava(self, bhairava: str) -> list[Temple]:
        return [t for t in self.temples.values() if t.bhairava == bhairava]

    def get_temples_by_domain(self, domain: str) -> list[Temple]:
        return [t for t in self.temples.values() if t.domain == domain]

    def get_active_temples(self) -> list[Temple]:
        return [t for t in self.temples.values() if t.status == "awake"]

    async def awaken_temple(self, temple_number: int) -> dict:
        """
        Awaken a single temple (start its MCP server process).
        Like lighting a lamp in a shrine — presence precedes function.
        """
        temple = self.temples.get(temple_number)
        if not temple:
            return {"error": f"Temple {temple_number} not found in registry"}

        script_path = self.base_dir / temple.script
        if not script_path.exists():
            return {
                "temple": temple.name,
                "status": "script_missing",
                "path": str(script_path),
                "note": f"Generate with: gemini_avatar_node.generate_temple_code('{temple.name.lower()}')",
            }

        # Check if API key is required and present
        if temple.env_key and not os.getenv(temple.env_key):
            return {
                "temple": temple.name,
                "status": "dormant_no_key",
                "required_env": temple.env_key,
                "note": f"Add {temple.env_key} to .env to awaken this temple",
            }

        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, str(script_path), "sse",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env={**os.environ, "MCP_PORT": str(temple.port)},
            )
            temple.process = proc
            temple.status = "awake"
            await asyncio.sleep(0.5)  # Give the server a moment to breathe
            return {
                "temple": temple.name,
                "number": temple.number,
                "bhairava": temple.bhairava,
                "status": "awake",
                "port": temple.port,
                "pid": proc.pid,
            }
        except Exception as e:
            temple.status = "error"
            return {"temple": temple.name, "status": "error", "error": str(e)}

    async def awaken_bhairava_hub(self, bhairava: str) -> list[dict]:
        """Awaken all temples under a Bhairava hub simultaneously."""
        temples = self.get_temples_by_bhairava(bhairava)
        tasks = [self.awaken_temple(t.number) for t in temples]
        return await asyncio.gather(*tasks)

    async def awaken_all(self) -> dict:
        """
        The Great Awakening — invoke all 65 temples.
        This is the moment the Nexus comes fully alive.
        """
        print("\n🕉️  NEXUS AWAKENING — All 65 Temples Rising...")
        print("    'Yato va imani bhutani jayante...'")
        print("    'That from which all beings arise...'\n")

        results = {}
        for bhairava in BHAIRAVA_HUBS:
            print(f"  ◈ Awakening {bhairava} Hub ({len(BHAIRAVA_HUBS[bhairava])} temples)...")
            hub_results = await self.awaken_bhairava_hub(bhairava)
            results[bhairava] = hub_results
            await asyncio.sleep(0.1)

        awake_count = sum(1 for t in self.temples.values() if t.status == "awake")
        print(f"\n  ✓ {awake_count} / 65 Temples Awake")
        print("  Om Namah Shivaya 🕉️\n")
        return {
            "status": "nexus_alive",
            "temples_awake": awake_count,
            "temples_total": 65,
            "hub_results": results,
        }

    async def nexus_pulse(self) -> dict:
        """
        The Nexus heartbeat — check all temples and return a status mandala.
        Like Shiva's damaru drum: the pulse that sustains all worlds.
        """
        status_map = {}
        async with httpx.AsyncClient(timeout=3.0) as client:
            tasks = []
            for temple in self.temples.values():
                tasks.append(self._check_temple_health(client, temple))
            results = await asyncio.gather(*tasks, return_exceptions=True)

        for temple, result in zip(self.temples.values(), results):
            status_map[temple.name] = {
                "number": temple.number,
                "bhairava": temple.bhairava,
                "status": result if isinstance(result, str) else "unreachable",
            }

        awake = sum(1 for v in status_map.values() if v["status"] == "healthy")
        return {
            "pulse": "ALIVE" if awake > 0 else "SILENT",
            "temples_healthy": awake,
            "temples_total": 65,
            "mandala": status_map,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        }

    async def _check_temple_health(self, client: httpx.AsyncClient, temple: Temple) -> str:
        if temple.status != "awake":
            return "dormant"
        try:
            resp = await client.get(f"http://localhost:{temple.port}/health")
            return "healthy" if resp.status_code == 200 else "degraded"
        except Exception:
            return "unreachable"

    async def route_to_bhairava(self, query: str, bhairava: str) -> dict:
        """
        Route a query to the appropriate Bhairava hub.
        The Sutradhra knows which face of Shiva to invoke.
        """
        temples = self.get_temples_by_bhairava(bhairava)
        awake = [t for t in temples if t.status == "awake"]

        if not awake:
            return {
                "error": f"No awake temples in {bhairava} hub",
                "hint": f"Run: await orchestrator.awaken_bhairava_hub('{bhairava}')",
            }
        # Route to the first awake temple in the hub (can be made smarter)
        target = awake[0]
        return {
            "routed_to": target.name,
            "bhairava": bhairava,
            "port": target.port,
            "query": query,
            "status": "routing_complete",
        }

    def generate_status_report(self) -> str:
        """Generate a beautiful ASCII mandala status report."""
        lines = [
            "",
            "╔═══════════════════════════════════════════════════════════╗",
            "║           NEXUS BHAIRAVA TEMPLES — STATUS MANDALA         ║",
            "╠═══════════════════════════════════════════════════════════╣",
        ]
        for bhairava, temple_nums in BHAIRAVA_HUBS.items():
            temples = [self.temples[n] for n in temple_nums]
            awake = [t for t in temples if t.status == "awake"]
            dormant = [t for t in temples if t.status != "awake"]
            lines.append(f"║  {bhairava:<12} ◈  {len(awake):>2}/{len(temples)} awake  "
                         f"{'█' * len(awake)}{'░' * len(dormant)}  ║")
        lines += [
            "╠═══════════════════════════════════════════════════════════╣",
            f"║  Total: {sum(1 for t in self.temples.values() if t.status == 'awake'):>2}/65 awake"
            f"  ·  Om Namah Shivaya 🕉️                  ║",
            "╚═══════════════════════════════════════════════════════════╝",
            "",
        ]
        return "\n".join(lines)

    async def shutdown_all(self):
        """Graceful shutdown — like the universe returning to Shiva's stillness."""
        print("\n🕉️  Returning all temples to silence...")
        for temple in self.temples.values():
            if temple.process and temple.status == "awake":
                temple.process.terminate()
                temple.status = "dormant"
        print("   All temples still. Shiva rests. Om.\n")


# ═══════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════

async def main():
    orchestrator = NexusOrchestrator()
    print(orchestrator.generate_status_report())

    mode = sys.argv[1] if len(sys.argv) > 1 else "pulse"

    if mode == "awaken":
        result = await orchestrator.awaken_all()
        print(json.dumps(result, indent=2))
    elif mode == "pulse":
        result = await orchestrator.nexus_pulse()
        print(json.dumps(result, indent=2))
    elif mode == "report":
        print(orchestrator.generate_status_report())


if __name__ == "__main__":
    asyncio.run(main())