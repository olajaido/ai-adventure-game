export const GAME_CONSTANTS = {
    MAX_HEALTH: 100,
    BASE_EXPERIENCE: 10,
    MAX_INVENTORY_SLOTS: 20,
    MAX_LEVEL: 50,
  };
  
  export const ITEM_TYPES = {
    WEAPON: 'weapon',
    ARMOR: 'armor',
    POTION: 'potion',
    SCROLL: 'scroll',
    ARTIFACT: 'artifact'
  };
  
  export const RARITIES = {
    COMMON: {
      name: 'Common',
      color: '#c0c0c0',
      multiplier: 1
    },
    UNCOMMON: {
      name: 'Uncommon',
      color: '#00ff00',
      multiplier: 1.5
    },
    RARE: {
      name: 'Rare',
      color: '#0000ff',
      multiplier: 2
    },
    EPIC: {
      name: 'Epic',
      color: '#800080',
      multiplier: 2.5
    },
    LEGENDARY: {
      name: 'Legendary',
      color: '#ffa500',
      multiplier: 3
    }
  };
  
  export const API_ENDPOINTS = {
    GAME_STATE: '/game-state',
    INVENTORY: '/inventory',
    USER_STATS: '/user-stats',
    GENERATE_STORY: '/generate-story',
    SAVE_GAME: '/save-game'
  };