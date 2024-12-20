// Calculate experience needed for next level
export const calculateNextLevelExp = (currentLevel) => {
    return currentLevel * 100;
  };
  
  // Calculate if player can level up
  export const checkLevelUp = (experience, currentLevel) => {
    const requiredExp = calculateNextLevelExp(currentLevel);
    return experience >= requiredExp;
  };
  
  // Calculate health percentage
  export const calculateHealthPercentage = (currentHealth, maxHealth = 100) => {
    return (currentHealth / maxHealth) * 100;
  };
  
  // Format large numbers
  export const formatNumber = (number) => {
    return new Intl.NumberFormat().format(number);
  };
  
  // Generate random item
  export const generateRandomItem = (playerLevel) => {
    const itemTypes = ['weapon', 'armor', 'potion'];
    const rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary'];
    
    const type = itemTypes[Math.floor(Math.random() * itemTypes.length)];
    const rarity = rarities[Math.floor(Math.random() * rarities.length)];
    
    return {
      type,
      rarity,
      level: playerLevel,
      power: playerLevel * (rarities.indexOf(rarity) + 1)
    };
  };