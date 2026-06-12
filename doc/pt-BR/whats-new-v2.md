# O que há de novo na v2.3/v2.4

Este guia resume os principais recursos adicionados em **stable v2.3** e **stable v2.4** do HotelRestaurantMini-MartManagement.

**Sites estáveis ativos:**

| Versão | URL |
|--------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Desenvolvimento** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Interface completa em 21 idiomas

A IU do aplicativo Web está disponível em **21 localidades**: inglês, espanhol, francês, alemão, japonês, coreano, árabe, hindi, tailandês, vietnamita, indonésio, turco, russo, italiano, holandês, polonês, hebraico, laosiano, português (Brasil), chinês (simplificado) e chinês (tradicional).

### Onde alterar o idioma

| Tela | Como |
|--------|-----|
| **Login/configuração** | Menu suspenso de idioma no cabeçalho (antes do login) |
| **Após login** | Seletor de localidade da barra superior ou **Localização** no menu |
| **Configurações** | Seção de idioma do aplicativo |

A preferência é salva no armazenamento do navegador (`hotel_mgr_uiLocale`).

### RTL (da direita para a esquerda)

**Árabe** e **Hebraico** ativam o layout RTL para todo o aplicativo. Os formulários modais usam alinhamento aprimorado para que rótulos e entradas sejam lidos corretamente nas linguagens LTR e RTL.

---

## Configuração inicial (traduzida)

O assistente de configuração está totalmente localizado:

- Nome da empresa/hotel
- Texto do cabeçalho do sistema
- Campos de nome de usuário, e-mail e senha do administrador
- Todos os botões e mensagens de validação

Após a configuração, o nome do hotel é armazenado e mostrado no cabeçalho do aplicativo onde configurado.

---

## Ações rápidas do painel (grade PMS)

O **Painel** mostra uma grade de botões azuis **+** para tarefas comuns:

| Botão | Abre |
|--------|--------|
| Adicionar quarto | Novo formulário de quarto |
| Adicionar reserva | Novo formulário de reserva |
| Adicionar convidado | Novo formulário de convidado |
| Adicionar tarefa | Novo ticket de manutenção |
| Adicionar serviço | Nova solicitação de serviço |
| Adicionar fatura | Novo formulário de fatura |
| Adicionar estoque | Novo item de inventário |
| Adicionar cardápio | Novo item de menu |
| Adicionar item da loja | Nova loja/item mini-mercado |
| Adicionar usuário | Nova conta de pessoal |

**Observação:** *Adicionar limpeza* e *Adicionar transação* foram removidos desta grade (v2.4). Use a barra lateral para **Housekeeping** e **Transactions** quando necessário.

---

## Formulários modais traduzidos

As caixas de diálogo de adição e edição estão localizadas em todos os 21 idiomas, incluindo:

- **Manutenção** — novo ticket (quarto, prioridade, emissão, notas)
- **Fatura** — adicionar/editar (hóspede, quarto, datas, valores, status do pagamento)
- **Inventário** — adicionar/editar item (nome, código de barras, categoria, quantidade, disponibilidade de PDV)
- **Item de menu** — adicionar/editar (nome, ícone, preço, categoria, imagem, link de estoque)
- **Item da loja** — adicionar/editar (nome, preço, categoria, ícone de prateleira, código de barras, estoque)- **Conta de usuário** — adicionar/editar (nome, e-mail, senha, função)

Os rótulos de upload de imagens (“do dispositivo”, “ou URL da imagem”) seguem o idioma ativo.

---

## Reserva → Novo hóspede

Ao criar uma **reserva**, caso o hóspede ainda não esteja no diretório:

1. Toque em **+ Novo hóspede** (ou equivalente) no formulário de reserva.
2. Preencha o modal **Novo Hóspede** (nome, passaporte, nacionalidade, data de nascimento, forma de pagamento, contato, notas).
3. Toque em **Adicionar hóspede e retornar** — você retorna à reserva com o novo hóspede selecionado.

O seletor de nacionalidade (lista de pesquisa) também é traduzido.

---

## Documentação

- Este guia de **Novidades** está disponível em todos os 21 idiomas de documentação.
- Abra documentos no aplicativo: **barra superior → Documentação**, **☰ Ajuda → Documentação** ou **navegação inferior → Documentos**.
- URL independente: `/doc/?lang={code}#/whats-new-v2`

---

## Para administradores

| Tarefa | Onde |
|------|--------|
| Treinar a equipe na mudança de idioma | [Localization](localization.md) |
| Configurar propriedade após atualização | [Settings & configuration](settings-and-configuration.md) |
| Implantar atualizações | [Deployment](deployment.md) — `npm run deploy:stable` publica em v2.3 e v2.4 |

---

## Guias relacionados

- [Localization](localization.md) — idiomas, RTL, arquivos de localidade
- [First-time setup](first-time-setup.md) — configuração inicial
- [Navigation & UI](navigation-and-ui.md) — painel, barra lateral, navegação móvel
- [Hotel operations](hotel-operations.md) — reservas e convidados
- [Deployment](deployment.md) — desenvolvimento vs estável v2.3 / v2.4