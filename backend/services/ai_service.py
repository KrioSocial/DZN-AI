# AI Service - handles all OpenAI API integrations
# Provides text generation, image generation, and analysis features

import openai
from openai import OpenAI
import os
import json

class AIService:
    """Service class for OpenAI API interactions"""
    
    def __init__(self, api_key):
        """
        Initialize OpenAI client with API key
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
    
    def generate_design_description(self, room_type, style, budget, keywords=None):
        """
        Generate AI design description and recommendations
        
        Args:
            room_type: Type of room (bedroom, living room, etc.)
            style: Design style (modern, minimalist, etc.)
            budget: Budget amount
            keywords: Additional keywords/requirements
        
        Returns:
            Dictionary with description and recommendations
        """
        try:
            # Build prompt for GPT-4
            prompt = f"""As an expert interior designer, create a detailed design concept for:
            
Room Type: {room_type}
Style: {style}
Budget: £{budget}
{f'Additional Requirements: {keywords}' if keywords else ''}

Please provide:
1. A detailed design description (2-3 paragraphs)
2. A color palette (5 colors with hex codes)
3. Key furniture pieces needed
4. Lighting recommendations
5. Styling tips

Format the response as JSON with keys: description, color_palette, furniture_list, lighting, styling_tips"""

            # Call OpenAI GPT-4 API
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert interior designer helping create beautiful, functional spaces."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract response content
            content = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to structured text
            try:
                result = json.loads(content)
            except:
                # If not valid JSON, create structured response
                result = {
                    'description': content,
                    'color_palette': [],
                    'furniture_list': [],
                    'lighting': '',
                    'styling_tips': ''
                }
            
            return result
            
        except Exception as e:
            print(f"Error generating design description: {e}")
            return None
    
    def generate_design_image(self, room_type, style, description):
        """
        Generate AI design image using DALL-E
        
        Args:
            room_type: Type of room
            style: Design style
            description: Design description for context
        
        Returns:
            URL of generated image or None
        """
        try:
            # Build image generation prompt
            prompt = f"Professional interior design photo: {style} style {room_type}, {description}. High quality, realistic, well-lit, magazine quality"
            
            # Call DALL-E API
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Extract image URL
            image_url = response.data[0].url
            return image_url
            
        except Exception as e:
            print(f"Error generating design image: {e}")
            return None
    
    def generate_moodboard(self, room_type, style, budget, keywords):
        """
        Generate complete moodboard with description, images, and colors
        
        Args:
            room_type: Type of room
            style: Design style
            budget: Budget amount
            keywords: Additional requirements
        
        Returns:
            Dictionary with complete moodboard data
        """
        # Generate text description first
        design_data = self.generate_design_description(room_type, style, budget, keywords)
        
        if not design_data:
            return None
        
        # Generate image based on description
        image_url = self.generate_design_image(room_type, style, design_data.get('description', ''))
        
        # Compile complete moodboard
        return {
            'description': design_data.get('description', ''),
            'image_urls': [image_url] if image_url else [],
            'color_palette': design_data.get('color_palette', []),
            'furniture_list': design_data.get('furniture_list', []),
            'lighting': design_data.get('lighting', ''),
            'styling_tips': design_data.get('styling_tips', '')
        }
    
    def analyze_message_sentiment(self, message_text):
        """
        Analyze sentiment of client message
        
        Args:
            message_text: The message to analyze
        
        Returns:
            Sentiment (positive, neutral, negative) and confidence
        """
        try:
            prompt = f"""Analyze the sentiment of this client message. Return only: positive, neutral, or negative.

Message: {message_text}

Sentiment:"""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            sentiment = response.choices[0].message.content.strip().lower()
            return sentiment
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return 'neutral'
    
    def summarize_message(self, message_text):
        """
        Generate summary of client message
        
        Args:
            message_text: The message to summarize
        
        Returns:
            Brief summary string
        """
        try:
            prompt = f"Summarize this client message in one concise sentence:\n\n{message_text}"
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Error summarizing message: {e}")
            return message_text[:100] + '...' if len(message_text) > 100 else message_text
    
    def generate_marketing_content(self, content_type, project_info, platform=None):
        """
        Generate marketing content for social media, blogs, or emails
        
        Args:
            content_type: Type of content (caption, blog, email, post)
            project_info: Dictionary with project details
            platform: Target platform (Instagram, LinkedIn, etc.)
        
        Returns:
            Generated content text
        """
        try:
            # Build prompt based on content type
            if content_type == 'caption':
                prompt = f"""Create an engaging Instagram caption for an interior design project:
                
Project: {project_info.get('title', '')}
Style: {project_info.get('style', '')}
Description: {project_info.get('description', '')}

Include relevant hashtags and keep it concise yet engaging."""
            
            elif content_type == 'blog':
                prompt = f"""Write a professional blog post about this interior design project:
                
Project: {project_info.get('title', '')}
Style: {project_info.get('style', '')}
Description: {project_info.get('description', '')}

Include sections on design inspiration, key features, and styling tips. 400-500 words."""
            
            elif content_type == 'email':
                prompt = f"""Write a professional email to showcase this interior design project to potential clients:
                
Project: {project_info.get('title', '')}
Style: {project_info.get('style', '')}
Description: {project_info.get('description', '')}

Keep it professional, engaging, and include a call-to-action."""
            
            else:  # general post
                prompt = f"""Create engaging social media content for {platform or 'social media'} about this interior design project:
                
Project: {project_info.get('title', '')}
Description: {project_info.get('description', '')}

Make it professional yet personable."""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a professional marketing copywriter specializing in interior design."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            return content
            
        except Exception as e:
            print(f"Error generating marketing content: {e}")
            return None
    
    def generate_project_insights(self, project_data):
        """
        Generate AI insights and suggestions for a project
        
        Args:
            project_data: Dictionary with project information
        
        Returns:
            Dictionary with insights and recommendations
        """
        try:
            prompt = f"""Analyze this interior design project and provide insights:
            
Project: {project_data.get('title', '')}
Status: {project_data.get('status', '')}
Budget: £{project_data.get('budget', 0)}
Spent: £{project_data.get('spent', 0)}
Deadline: {project_data.get('deadline', 'Not set')}

Provide:
1. Budget analysis (are they on track?)
2. Timeline recommendations
3. Potential issues or missing elements
4. Next steps suggestions

Format as JSON with keys: budget_analysis, timeline_recommendation, potential_issues, next_steps"""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping interior designers manage projects efficiently."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=600
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                insights = json.loads(content)
            except:
                insights = {'analysis': content}
            
            return insights
            
        except Exception as e:
            print(f"Error generating project insights: {e}")
            return None

