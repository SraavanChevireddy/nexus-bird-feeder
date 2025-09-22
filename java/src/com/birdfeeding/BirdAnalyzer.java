package com.birdfeeding;

import java.util.*;
import java.io.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

/**
 * Bird Feeding Pattern Analyzer
 * Demonstrates Java integration with Python bird feeding API
 */
public class BirdAnalyzer {
    
    private ObjectMapper objectMapper;
    
    public BirdAnalyzer() {
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Analyze feeding patterns from JSON data
     */
    public String analyzePatterns(String jsonData) {
        try {
            JsonNode feedingData = objectMapper.readTree(jsonData);
            
            Map<String, Object> analysis = new HashMap<>();
            Map<String, Object> patterns = new HashMap<>();
            List<String> recommendations = new ArrayList<>();
            
            // Analyze bird types
            Map<String, Integer> birdCounts = new HashMap<>();
            Map<String, Integer> foodCounts = new HashMap<>();
            List<Integer> quantities = new ArrayList<>();
            
            for (JsonNode feeding : feedingData) {
                String birdType = feeding.get("bird_type").asText();
                String foodType = feeding.get("food_type").asText();
                int quantity = feeding.get("quantity").asInt();
                
                birdCounts.put(birdType, birdCounts.getOrDefault(birdType, 0) + 1);
                foodCounts.put(foodType, foodCounts.getOrDefault(foodType, 0) + 1);
                quantities.add(quantity);
            }
            
            // Find most common bird and food
            String mostCommonBird = birdCounts.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse("Unknown");
                
            String preferredFood = foodCounts.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse("Unknown");
            
            // Calculate statistics
            double avgQuantity = quantities.stream()
                .mapToInt(Integer::intValue)
                .average()
                .orElse(0.0);
            
            patterns.put("most_common_bird", mostCommonBird);
            patterns.put("preferred_food", preferredFood);
            patterns.put("average_quantity", Math.round(avgQuantity * 100.0) / 100.0);
            patterns.put("total_feedings", feedingData.size());
            patterns.put("bird_diversity", birdCounts.size());
            patterns.put("food_variety", foodCounts.size());
            
            // Generate recommendations
            if (birdCounts.size() < 3) {
                recommendations.add("Consider adding more food variety to attract different bird species");
            }
            if (avgQuantity > 50) {
                recommendations.add("High feeding quantities detected - monitor for waste");
            }
            if (mostCommonBird.equals("Robin")) {
                recommendations.add("Robins prefer worms and berries - consider adding these options");
            }
            
            analysis.put("patterns", patterns);
            analysis.put("recommendations", recommendations);
            analysis.put("analysis_engine", "Java Bird Analyzer v1.0");
            analysis.put("processed_by", "Native Java");
            analysis.put("timestamp", System.currentTimeMillis());
            
            return objectMapper.writeValueAsString(analysis);
            
        } catch (Exception e) {
            return "{\"error\": \"" + e.getMessage() + "\"}";
        }
    }
    
    /**
     * Command line interface for standalone execution
     */
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java BirdAnalyzer <json_file>");
            System.exit(1);
        }
        
        try {
            String jsonContent = new String(java.nio.file.Files.readAllBytes(
                java.nio.file.Paths.get(args[0])));
            
            BirdAnalyzer analyzer = new BirdAnalyzer();
            String result = analyzer.analyzePatterns(jsonContent);
            
            System.out.println(result);
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
