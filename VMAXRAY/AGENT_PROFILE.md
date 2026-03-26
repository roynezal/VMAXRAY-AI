# VMAXRAY Agent Profile
*Last updated: 2026-03-26*

## 📊 Current Project State

### Version Status
| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `VMAXRAY_PRO_CHART-9_V9.9_final.html` | 3034 | ✅ **FIXED** | Complete Entry Matrix 13 gates, all bugs fixed |
| `VMAXRAY_PRO_CHART-9.9.html` | 2823 | 🔄 **NEEDS FIXES** | Array access bugs, missing Entry Matrix |

### Key Features Implemented
- ✅ **Entry Matrix 13 Gates**: Static object with News, NoPos, Sqz, HTFSqz, EWValid, Session, BBTrend, Basis, FibZone, Bounce, Chase, TPDist
- ✅ **Awareness Display**: %B, Vol, Fib, Sqz, EW, Risk metrics
- ✅ **Session Pills**: SYD/TOK/LON/NY with solid green when active
- ✅ **Null Safety**: Comprehensive DOM element null checks
- ✅ **Bug Fixes**: Array access fixed (`[4]` → `.c`)

### Critical Bugs Fixed
1. `checkEntryGates()`: `S.K[S.K.length-1][4]` → `S.K[S.K.length-1].c`
2. `autoMonitor()`: Same fix
3. `updateBBState()`: `c[4]` → `c.c`, `c[1]` → `c.o`, `c[2]` → `c.h`
4. `EntryMatrix.evaluate()`: `K[n-1][4]` → `K[n-1].c`

## 🔧 Configuration

### AI Providers
| Provider | Model | Status | Authentication |
|----------|-------|--------|----------------|
| **Google** | `google/gemini-2.5-flash` | ✅ Working | API Key: `AIzaSyCf9c1F_a7AisDzgsjXhAfS-0OtHRLeE6k` |
| **GitHub Copilot** | `github-copilot/claude-haiku-4.5` | ✅ Working | OAuth: `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` |
| **Opencode Zen** | `opencode/mimo-v2-omni-free` | ✅ Available | Free (rate limited) |
| **DeepSeek** | `deepseek/deepseek-reasoner` | ✅ Available | Uses credits |

### Git Repository
- **Remote**: `git@github.com:roynezal/VMAXRAY-AI.git`
- **SSH**: ✅ Configured and working
- **Last Commit**: "Fix array access bugs in EntryMatrix and trading functions, add awareness metrics, ensure gates start unchecked per AGENTS.md specs"
- **Branch**: `main`

### Desktop Shortcuts
4 shortcuts created on Desktop:
1. `opencode-google.desktop` - Google Gemini 2.5 Flash
2. `opencode-copilot.desktop` - GitHub Copilot Claude Haiku 4.5
3. `opencode-zen.desktop` - Opencode Mimo V2 Omni Free
4. `opencode-deepseek.desktop` - DeepSeek Reasoner

## 🎯 Immediate Next Tasks

### Priority 1: Fix Older Version (`VMAXRAY_PRO_CHART-9.9.html`)
```javascript
// Line 2787: checkEntryGates()
S.K[S.K.length-1][4] → S.K[S.K.length-1].c

// Line 2790: autoMonitor()  
S.K[S.K.length-1][4] → S.K[S.K.length-1].c

// Line 2805: updateBBState()
c[4] → c.c, c[1] → c.o, c[2] → c.h, c[3] → c.l

// Line 2810: Another array access
S.K[S.K.length-1][4] → S.K[S.K.length-1].c
```

### Priority 2: Port Entry Matrix to Older Version
- Copy EntryMatrix static object (lines 2693-2831 from final.html)
- Ensure `updateMatrix()` calls EntryMatrix.evaluate() and EntryMatrix.render()
- Add awareness metrics display

### Priority 3: Test Both Versions
- Open `file:///home/live/VMAXRAY/VMAXRAY_PRO_CHART-9.9.html` in browser
- Verify chart loads without JavaScript errors
- Test Entry Matrix toggle functionality
- Check session pills show correct active sessions

## 🤖 AI Provider Commands

### Quick Start Commands
```bash
# Google Gemini (recommended - free)
opencode run --model google/gemini-2.5-flash

# GitHub Copilot (free OAuth)
opencode run --model github-copilot/claude-haiku-4.5

# Opencode Zen (free, rate limited)
opencode run --model opencode/mimo-v2-omni-free

# DeepSeek (uses credits)
opencode run --model deepseek/deepseek-reasoner
```

### Environment Variable
```bash
export OPENCODE_MODEL=google/gemini-2.5-flash
opencode
```

## 📁 File Structure

### Key Files
- `VMAXRAY_PRO_CHART-9_V9.9_final.html` - Main fixed version
- `VMAXRAY_PRO_CHART-9.9.html` - Older version needing fixes
- `AGENTS.md` - Session history and lessons learned
- `NEXT_SESSION_TODO.md` - Detailed next steps
- `AGENT_PROFILE.md` - This file (current state)

### Configuration Files
- `~/.local/share/opencode/auth.json` - AI provider credentials
- `~/.ssh/id_ed25519` - SSH private key (GitHub)
- `~/.ssh/id_ed25519.pub` - SSH public key

### Desktop Shortcuts
- `~/Desktop/opencode-*.sh` - Shell scripts
- `~/Desktop/opencode-*.desktop` - Desktop launchers
- `~/Desktop/README-AI-Shortcuts.txt` - Usage guide

## ⚠️ Known Issues

### Older Version Bugs
1. **Array access errors**: Using array indices `[4]` instead of object properties `.c`
2. **Missing Entry Matrix**: No 13-gate EntryMatrix implementation
3. **No awareness display**: Missing %B, Vol, Fib, Sqz, EW, Risk metrics

### Session Notes
- **Entry Matrix gates start UNCHECKED**: User must manually enable gates
- **Session pills**: Solid green when active, no glow effect
- **Google API**: Tested and working with Gemini 2.5 Flash
- **GitHub Copilot**: OAuth token configured and working

## 🔄 Workflow for Next Session

1. **Start with AI provider** - Use Google Gemini (free) or GitHub Copilot
2. **Fix older version** - Apply array access fixes
3. **Port Entry Matrix** - Copy from final version
4. **Test both versions** - Verify functionality matches
5. **Update documentation** - Add any new findings

---

*Profile created: 2026-03-26*
*Ready for next session with any AI provider*